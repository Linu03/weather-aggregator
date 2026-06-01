import respx

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

GEOCODING_OK = {
    "results": [
        {
            "latitude": 45.75,
            "longitude": 21.23,
            "name": "Timisoara",
            "country": "Romania",
        }
    ]
}

FORECAST_OK = {
    "current_weather": {
        "temperature": 22.4,
        "windspeed": 14.2,
        "weathercode": 3,
        "time": "2024-06-01T14:00",
    }
}


def stub_open_meteo_success() -> None:
    respx.get(GEOCODING_URL).respond(json=GEOCODING_OK)
    respx.get(FORECAST_URL).respond(json=FORECAST_OK)


def stub_city_not_found() -> None:
    respx.get(GEOCODING_URL).respond(json={"results": []})


def stub_open_meteo_unavailable() -> None:
    respx.get(GEOCODING_URL).respond(status_code=503)
