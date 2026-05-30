from domain.ports import WeatherAPIPort, WeatherRepoPort
from domain.model import WeatherReading


class WeatherService:
    def __init__(self, api_port: WeatherAPIPort, repo_port:WeatherRepoPort):
        self.api_port = api_port
        self.repo_port = repo_port

    def fetch_and_store(self, city: str) -> WeatherReading:
        reading = delf.api_port.get_weather(city)
        saved = self.repo_port.save(reading)
        return saved
