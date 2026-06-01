from datetime import datetime, timedelta

import psycopg2

from domain.model import WeatherReading


def _reading(city: str, temperature: float, fetched_at: datetime) -> WeatherReading:
    return WeatherReading(
        city=city,
        temperature=temperature,
        wind_speed=10.0,
        description="Clear sky",
        fetched_at=fetched_at,
    )


def test_save_persists_reading(repo, postgres_container):
    from db_helper import db_params

    fetched_at = datetime(2024, 6, 1, 14, 0, 0)
    reading = _reading("Timisoara", 22.4, fetched_at)

    repo.save(reading)

    conn = psycopg2.connect(**db_params(postgres_container))
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT city, temperature, wind_speed, description, fetched_at
                FROM weather_reading
                WHERE city = %s
                """,
                ("Timisoara",),
            )
            row = cursor.fetchone()
    finally:
        conn.close()

    assert row is not None
    assert row[0] == "Timisoara"
    assert row[1] == 22.4
    assert row[2] == 10.0
    assert row[3] == "Clear sky"
    assert row[4] == fetched_at


def test_get_by_city_returns_all_readings_newest_first(repo):
    base = datetime(2024, 6, 1, 10, 0, 0)
    for temp, offset in [(20.0, 0), (21.0, 1), (22.0, 2)]:
        repo.save(_reading("Timisoara", temp, base + timedelta(hours=offset)))

    result = repo.get_by_city("Timisoara")

    assert len(result) == 3
    assert [r.temperature for r in result] == [22.0, 21.0, 20.0]
    assert result[0].fetched_at > result[1].fetched_at > result[2].fetched_at


def test_get_by_city_does_not_mix_cities(repo):
    base = datetime(2024, 6, 1, 10, 0, 0)
    repo.save(_reading("Timisoara", 20.0, base))
    repo.save(_reading("Madrid", 31.0, base + timedelta(hours=1)))

    timisoara = repo.get_by_city("Timisoara")
    madrid = repo.get_by_city("Madrid")

    assert len(timisoara) == 1
    assert timisoara[0].city == "Timisoara"
    assert timisoara[0].temperature == 20.0
    assert len(madrid) == 1
    assert madrid[0].city == "Madrid"
    assert madrid[0].temperature == 31.0


def test_get_latest_returns_most_recent_reading(repo):
    base = datetime(2024, 6, 1, 10, 0, 0)
    repo.save(_reading("Timisoara", 18.0, base))
    repo.save(_reading("Timisoara", 20.0, base + timedelta(hours=1)))
    newest = _reading("Timisoara", 25.0, base + timedelta(hours=2))
    repo.save(newest)

    latest = repo.get_latest("Timisoara")

    assert latest is not None
    assert latest.temperature == 25.0
    assert latest.fetched_at == newest.fetched_at


def test_get_latest_unknown_city_returns_none(repo):
    assert repo.get_latest("UnknownCity") is None
