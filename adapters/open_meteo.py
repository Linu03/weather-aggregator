import httpx
from domain.ports import WeatherApiPort
from domain.model import WeatherReading
from domain.errors import CityNotFoundError, ExternalApiError

WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Icy fog",
    51: "Drizzle: light",
    53: "Drizzle: moderate",
    55: "Drizzle: heavy",
    61: "Rain: slight",
    63: "Rain: moderate",
    65: "Rain: heavy",
    71: "Snow: slight",
    73: "Snow: moderate",
    75: "Snow: heavy",
    80: "Showers: slight",
    81: "Showers: moderate",
    82: "Showers: heavy",
    95: "Thunderstorm",
    99: "Thunderstorm with hail",
}


class OpenMeteoAdapter(WeatherApiPort):
    def __init__(
        self,
        geocoding_base_url: str = "https://geocoding-api.open-meteo.com",
        forecast_base_url: str = "https://api.open-meteo.com",
    ):
        self._geocoding_base_url = geocoding_base_url.rstrip("/")
        self._forecast_base_url = forecast_base_url.rstrip("/")

    def get_weather(self, city: str) -> WeatherReading:
        try:
            geo_response = httpx.get(
                f"{self._geocoding_base_url}/v1/search",
                params={"name": city, "count": 1, "language": "en", "format": "json"},
                timeout=10.0,
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()
        except httpx.HTTPError as e:
            raise ExternalApiError("Open-Meteo geocoding unavailable") from e

        if not geo_data.get("results"):
            raise CityNotFoundError(f"City not found: {city}")

        location = geo_data["results"][0]
        canonical_city = location["name"]
        lat = location["latitude"]
        lon = location["longitude"]

        try:
            weather_response = httpx.get(
                f"{self._forecast_base_url}/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current_weather": True,
                    "wind_speed_unit": "kmh",
                },
                timeout=10.0,
            )
            weather_response.raise_for_status()
            weather_data = weather_response.json()["current_weather"]
        except httpx.HTTPError as e:
            raise ExternalApiError("Open-Meteo weather unavailable") from e
        except (KeyError, TypeError) as e:
            raise ExternalApiError("Invalid Open-Meteo weather response") from e

        return WeatherReading(
            city=canonical_city,
            temperature=weather_data["temperature"],
            wind_speed=weather_data["windspeed"],
            description=WMO_CODES.get(weather_data["weathercode"], "Unknown"),
        )
