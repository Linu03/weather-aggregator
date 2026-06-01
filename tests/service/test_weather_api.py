import respx

from stubs import stub_city_not_found, stub_open_meteo_success, stub_open_meteo_unavailable


@respx.mock
def test_fetch_stores_reading_and_get_returns_it(client):
    stub_open_meteo_success()

    fetch = client.post("/weather/fetch", params={"city": "Timisoara"})
    assert fetch.status_code == 201
    assert fetch.json()["city"] == "Timisoara"
    assert fetch.json()["temperature"] == 22.4

    history = client.get("/weather/Timisoara")
    assert history.status_code == 200
    assert len(history.json()) == 1
    assert history.json()[0]["temperature"] == 22.4


@respx.mock
def test_fetch_unknown_city_returns_404(client):
    stub_city_not_found()

    response = client.post("/weather/fetch", params={"city": "UnknownCity"})
    assert response.status_code == 404

    history = client.get("/weather/UnknownCity")
    assert history.status_code == 200
    assert history.json() == []


@respx.mock
def test_fetch_when_open_meteo_unavailable_returns_503(client):
    stub_open_meteo_unavailable()

    response = client.post("/weather/fetch", params={"city": "Timisoara"})
    assert response.status_code == 503

    history = client.get("/weather/Timisoara")
    assert history.status_code == 200
    assert history.json() == []
