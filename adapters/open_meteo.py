import httpx
from domain.ports import WeatherApiPort
from domain.model import WeatherReading

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
    def get_weather(self, city: str) -> WeatherReading:
        geo_response = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"}
        )
        geo_data = geo_response.json()


         if not geo_data.get("results"):
            raise ValueError(f"City not found: {city}")

        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]

        weather_response = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True, "wind_speed_unit": "kmh"}
        )

        weather_data = weather_response.json()["current_weather"]

        return WeatherReading(
            city=city,
            temperature=weather_data["temperature"],
            wind_speed=weather_data["windspeed"],
            description=WMO_CODES.get(weather_data["weathercode"], "Unknown"),
        )