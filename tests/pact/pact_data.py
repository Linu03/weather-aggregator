CONSUMER = "weather-aggregator"
PROVIDER = "open-meteo"

LAT = 45.75
LON = 21.23

GEOCODING_RESPONSE = {
    "results": [
        {"latitude": LAT, "longitude": LON, "name": "Timisoara", "country": "Romania"}
    ]
}

FORECAST_RESPONSE = {
    "current_weather": {
        "temperature": 22.4,
        "windspeed": 14.2,
        "weathercode": 3,
        "time": "2024-06-01T14:00",
    }
}
