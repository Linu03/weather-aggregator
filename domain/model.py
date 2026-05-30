from dataclasses import dataclass, field
from datetime import datetime



@dataclass
class WeatherReading:
    city: str
    temperature: float
    wind_speed: float
    description: str
    fetched_at: datetime = field(default_factory=datetime.utcnow)


