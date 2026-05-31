from typing import List, Optional
from abc import ABC, abstractmethod
from domain.model import WeatherReading



class WeatherApiPort(ABC):
    @abstractmethod
    def get_weather(self, city:str) -> WeatherReading:
        pass

class WeatherRepoPort(ABC):

    @abstractmethod
    def save(self, reading: WeatherReading) -> WeatherReading:
        pass
    
    @abstractmethod
    def get_by_city(self, city: str) -> List[WeatherReading]:
        pass

    @abstractmethod
    def get_latest(self, city: str) -> Optional[WeatherReading]:
        pass