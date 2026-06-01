from datetime import datetime
from unittest.mock import MagicMock

import pytest

from domain.errors import CityNotFoundError, ExternalApiError
from domain.model import WeatherReading
from domain.service import WeatherService


@pytest.fixture
def api_port():
    return MagicMock()


@pytest.fixture
def repo_port():
    return MagicMock()


@pytest.fixture
def service(api_port, repo_port):
    return WeatherService(api_port=api_port, repo_port=repo_port)


def test_fetch_and_store_success(service, api_port, repo_port):
    reading = WeatherReading(
        city="Timisoara",
        temperature=22.4,
        wind_speed=14.2,
        description="Overcast",
        fetched_at=datetime(2024, 6, 1, 14, 0, 0),
    )
    api_port.get_weather.return_value = reading
    repo_port.save.return_value = reading

    result = service.fetch_and_store("Timisoara")

    api_port.get_weather.assert_called_once_with("Timisoara")
    repo_port.save.assert_called_once_with(reading)
    assert result == reading
    assert result.city == "Timisoara"
    assert result.temperature == 22.4
    assert result.wind_speed == 14.2
    assert result.description == "Overcast"


def test_fetch_and_store_external_api_failure(service, api_port, repo_port):
    api_port.get_weather.side_effect = ExternalApiError("Open-Meteo unavailable")

    with pytest.raises(ExternalApiError, match="Open-Meteo unavailable"):
        service.fetch_and_store("Timisoara")

    api_port.get_weather.assert_called_once_with("Timisoara")
    repo_port.save.assert_not_called()


def test_fetch_and_store_city_not_found(service, api_port, repo_port):
    api_port.get_weather.side_effect = CityNotFoundError("City not found: Timisoara")

    with pytest.raises(CityNotFoundError, match="City not found"):
        service.fetch_and_store("Timisoara")

    api_port.get_weather.assert_called_once_with("Timisoara")
    repo_port.save.assert_not_called()
