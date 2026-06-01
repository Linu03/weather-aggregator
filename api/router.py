from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import List
from datetime import datetime

from domain.service import WeatherService
from domain.errors import CityNotFoundError, ExternalApiError
from adapters.open_meteo import OpenMeteoAdapter
from adapters.postgres_repo import PostgresWeatherRepo
import os


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

    # Adapter pentru Open-Meteo API
    api_adapter = OpenMeteoAdapter()
    
    repo_adapter = PostgresWeatherRepo(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    return WeatherService(api_port=api_adapter, repo_port=repo_adapter)


@router.post("/fetch", response_model=WeatherResponse, status_code=201)
def fetch_weather(
    city: str = Query(..., description="Numele orașului pentru care se doresc datele meteo"),
    service: WeatherService = Depends(get_weather_service)
):

    try:
        reading = service.fetch_and_store(city)
        return WeatherResponse(
            city=reading.city,
            temperature=reading.temperature,
            wind_speed=reading.wind_speed,
            description=reading.description,
            fetched_at=reading.fetched_at
        )
    except CityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ExternalApiError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{city}", response_model=List[WeatherResponse])
def get_weather_by_city(
    city: str,
    service: WeatherService = Depends(get_weather_service)
):

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


@router.get("/{city}/latest", response_model=WeatherResponse)
def get_latest_weather(
    city: str,
    service: WeatherService = Depends(get_weather_service)
):

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
