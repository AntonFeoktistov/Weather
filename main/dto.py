from dataclasses import dataclass


@dataclass
class LocationDto:
    name_en: str = ""
    name_ru: str = ""
    state: str = ""
    lon: float = 0
    lat: float = 0


@dataclass
class WeatherDto:
    location: LocationDto = None
    temperature: float = 0
    description: str = ""
    wind_speed: float = 0
