import requests
import logging
from django.conf import settings
from main.dto import LocationDto, WeatherDto
from main.service.errors import WeatherNotFoundError
from main.service.serializer import Serializer

logger = logging.getLogger(__name__)


class WeatherFinder:
    def __init__(self):
        self.serializer = Serializer()

    def get_weather_by_city_name(self, city_name):

        location = self._get_location_by_city_name(city_name)
        weather = self.get_weather_by_location(location)
        if not weather.location:
            raise WeatherNotFoundError()
        return weather

    def _get_location_by_city_name(self, city_name):

        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {"q": city_name, "limit": 5, "appid": settings.OPENWEATHER_API_KEY}

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            locations = response.json()

            if not locations:
                logger.info(f"Город '{city_name}' не найден")
                return self._make_error_location_dto()

            loc = locations[0]

            local_names = loc.get("local_names", {})
            name_ru = local_names.get("ru", loc.get("name"))

            result = {
                "lat": round(loc["lat"], 3),
                "lon": round(loc["lon"], 3),
                "name_en": loc["name"],
                "name_ru": name_ru,
                "state": loc.get("state"),
            }

            return self.serializer.make_location_dto(result)

        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            return self._make_error_location_dto()

    def get_weather_by_location(self, location: LocationDto):

        if not location.name_en:
            return self._make_error_weather_dto()

        lat, lon = location.lat, location.lon
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric",
            "lang": "ru",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if data.get("cod") != 200:
                return self._make_error_weather_dto()

            result = {
                "location": location,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
            }

            return self.serializer.make_weather_dto(result)

        except Exception as e:
            logger.error(f"Weather error: {e}")
            return self._make_error_weather_dto()

    def _make_error_location_dto(self):
        return LocationDto()

    def _make_error_weather_dto(self):
        return WeatherDto()
