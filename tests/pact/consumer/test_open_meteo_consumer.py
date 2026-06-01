import socket
from pathlib import Path

import pytest
from pact import Consumer, Provider

from adapters.open_meteo import OpenMeteoAdapter
from pact_data import CONSUMER, FORECAST_RESPONSE, GEOCODING_RESPONSE, LAT, LON, PROVIDER

PACT_DIR = Path(__file__).resolve().parent.parent / "pacts"


@pytest.fixture(scope="module")
def pact():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]

    pact = Consumer(CONSUMER).has_pact_with(
        Provider(PROVIDER),
        host_name="127.0.0.1",
        port=port,
        pact_dir=str(PACT_DIR),
    )
    (
        pact.given("a city exists in geocoding")
        .upon_receiving("a geocoding request for a city name")
        .with_request(
            "GET",
            "/v1/search",
            query={"name": "Timisoara", "count": "1", "language": "en", "format": "json"},
        )
        .will_respond_with(200, body=GEOCODING_RESPONSE)
    )
    (
        pact.given("current weather is available for coordinates")
        .upon_receiving("a current weather forecast request")
        .with_request(
            "GET",
            "/v1/forecast",
            query={
                "latitude": str(LAT),
                "longitude": str(LON),
                "current_weather": "true",
                "wind_speed_unit": "kmh",
            },
        )
        .will_respond_with(200, body=FORECAST_RESPONSE)
    )
    pact.start_service()
    yield pact
    pact.stop_service()


def test_open_meteo_consumer_contract(pact):
    adapter = OpenMeteoAdapter(
        geocoding_base_url=pact.uri,
        forecast_base_url=pact.uri,
    )
    with pact:
        reading = adapter.get_weather("Timisoara")

    assert reading.temperature == FORECAST_RESPONSE["current_weather"]["temperature"]
