from fastapi.testclient import TestClient

from adapters.open_meteo import OpenMeteoAdapter
from adapters.postgres_repo import PostgresWeatherRepo
from api.router import get_weather_service
from domain.service import WeatherService
from main import app


def create_test_client(db: dict) -> TestClient:
    def override_get_weather_service() -> WeatherService:
        return WeatherService(
            api_port=OpenMeteoAdapter(),
            repo_port=PostgresWeatherRepo(
                host=db["host"],
                port=db["port"],
                database=db["database"],
                user=db["user"],
                password=db["password"],
            ),
        )

    app.dependency_overrides[get_weather_service] = override_get_weather_service
    return TestClient(app)


def clear_test_client() -> None:
    app.dependency_overrides.clear()
