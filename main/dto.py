from dataclasses import dataclass


@dataclass
class LocationDto:
    name: str
    long: float
    lat: float


@dataclass
class WeatherDto:
    city: str
    temperature: float
    description: str
    wind_speed: float
