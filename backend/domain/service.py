from typing import List, Optional
from domain.ports import WeatherApiPort, WeatherRepoPort
from domain.model import WeatherReading


class WeatherService:
    def __init__(self, api_port: WeatherApiPort, repo_port: WeatherRepoPort):
        self.api_port = api_port
        self.repo_port = repo_port

    def fetch_and_store(self, city: str) -> WeatherReading:
        reading = self.api_port.get_weather(city)
        saved = self.repo_port.save(reading)
        return saved

    def get_by_city(self, city: str) -> List[WeatherReading]:
        return self.repo_port.get_by_city(city)

    def get_latest(self, city: str) -> Optional[WeatherReading]:
        return self.repo_port.get_latest(city)
