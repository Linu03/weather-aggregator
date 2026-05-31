import psycopg2
from typing import List, Optional
from domain.ports import WeatherRepoPort
from domain.model import WeatherReading


class PostgresWeatherRepo(WeatherRepoPort):
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def _get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def save(self, reading: WeatherReading) -> WeatherReading:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO weather_reading (city, temperature, wind_speed, description, fetched_at)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (reading.city, reading.temperature, reading.wind_speed, reading.description, reading.fetched_at)
                )
                conn.commit()
            return reading
        finally:
            conn.close()

    def get_by_city(self, city: str) -> List[WeatherReading]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT city, temperature, wind_speed, description, fetched_at
                    FROM weather_reading
                    WHERE city = %s
                    ORDER BY fetched_at DESC
                    """,
                    (city,)
                )
                rows = cursor.fetchall()
                return [
                    WeatherReading(
                        city=row[0],
                        temperature=row[1],
                        wind_speed=row[2],
                        description=row[3],
                        fetched_at=row[4]
                    )
                    for row in rows
                ]
        finally:
            conn.close()

    def get_latest(self, city: str) -> Optional[WeatherReading]:
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT city, temperature, wind_speed, description, fetched_at
                    FROM weather_reading
                    WHERE city = %s
                    ORDER BY fetched_at DESC
                    LIMIT 1
                    """,
                    (city,)
                )
                row = cursor.fetchone()
                if row:
                    return WeatherReading(
                        city=row[0],
                        temperature=row[1],
                        wind_speed=row[2],
                        description=row[3],
                        fetched_at=row[4]
                    )
                return None
        finally:
            conn.close()
