from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List
from datetime import datetime

from domain.service import WeatherService
from adapters.open_meteo import OpenMeteoAdapter
from adapters.postgres_repo import PostgresWeatherRepo
import os


# Pydantic model pentru response
class WeatherResponse(BaseModel):
    city: str
    temperature: float
    wind_speed: float
    description: str
    fetched_at: datetime

    class Config:
        from_attributes = True


# Router
router = APIRouter(prefix="/weather", tags=["weather"])


# Dependency Injection - creează instanțe ale adapters și service
def get_weather_service() -> WeatherService:
    """
    Dependency injection pentru WeatherService
    Creează instanțe ale adapters cu configurația necesară
    """
    # Adapter pentru Open-Meteo API
    api_adapter = OpenMeteoAdapter()
    
    # Adapter pentru PostgreSQL (citește credențiale din environment)
    repo_adapter = PostgresWeatherRepo(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "weather_db"),
        user=os.getenv("DB_USER", "weather_user"),
        password=os.getenv("DB_PASSWORD", "weather_pass")
    )
    
    # Service cu dependency injection
    return WeatherService(api_port=api_adapter, repo_port=repo_adapter)


# Endpoint 1: POST /weather/fetch?city=Timisoara - Preia date meteo și le salvează
@router.post("/fetch", response_model=WeatherResponse, status_code=201)
def fetch_weather(
    city: str = Query(..., description="Numele orașului pentru care se doresc datele meteo"),
    service: WeatherService = Depends(get_weather_service)
):
    """
    Preia datele meteo de la Open-Meteo API pentru un oraș și le salvează în baza de date.
    
    - **city**: Query parameter - numele orașului
    
    Returns: WeatherReading salvat în baza de date
    """
    try:
        reading = service.fetch_and_store(city)
        return WeatherResponse(
            city=reading.city,
            temperature=reading.temperature,
            wind_speed=reading.wind_speed,
            description=reading.description,
            fetched_at=reading.fetched_at
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Endpoint 2: GET /weather/{city} - Toate citirile pentru un oraș
@router.get("/{city}", response_model=List[WeatherResponse])
def get_weather_by_city(
    city: str,
    service: WeatherService = Depends(get_weather_service)
):
    """
    Returnează toate citirile meteo pentru un oraș, ordonate descrescător după dată.
    
    - **city**: Numele orașului
    
    Returns: Lista de WeatherReading (poate fi goală)
    """
    try:
        readings = service.get_by_city(city)
        return [
            WeatherResponse(
                city=r.city,
                temperature=r.temperature,
                wind_speed=r.wind_speed,
                description=r.description,
                fetched_at=r.fetched_at
            )
            for r in readings
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


# Endpoint 3: GET /weather/{city}/latest - Ultima citire pentru un oraș
@router.get("/{city}/latest", response_model=WeatherResponse)
def get_latest_weather(
    city: str,
    service: WeatherService = Depends(get_weather_service)
):
    """
    Returnează ultima citire meteo pentru un oraș.
    
    - **city**: Numele orașului
    
    Returns: WeatherReading sau 404 dacă nu există date
    """
    try:
        reading = service.get_latest(city)
        if reading is None:
            raise HTTPException(status_code=404, detail=f"No weather data found for city: {city}")
        
        return WeatherResponse(
            city=reading.city,
            temperature=reading.temperature,
            wind_speed=reading.wind_speed,
            description=reading.description,
            fetched_at=reading.fetched_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
