import requests
import logging
from django.conf import settings
from django.core.cache import cache

from main.dto import WeatherDto

logger = logging.getLogger(__name__)


def get_weather_by_coords(lat, lon):

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
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            return

        city_name = get_location_name(lat, lon, data.get("name", "Неизвестно"))
        result = {
            "city": city_name,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }

        print(result)
        return make_weather_dto(result)

    except requests.exceptions.Timeout:
        logger.error(f"Timeout при запросе погоды для координат {lat}, {lon}")
        return {"success": False, "error": "Сервер не отвечает. Попробуйте позже."}
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса: {e}")
        return {"success": False, "error": "Ошибка соединения с сервером погоды"}
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return {"success": False, "error": "Произошла непредвиденная ошибка"}


def make_weather_dto(data: str) -> WeatherDto:
    city = data.get("city", "")
    temperature = data.get("temperature", 0)
    description = data.get("description", "")
    wind_speed = data.get("wind_speed", 0)
    return WeatherDto(
        city=city,
        temperature=temperature,
        description=description,
        wind_speed=wind_speed,
    )


def get_location_name(lat: float, lon: float, default: str):

    geo_url = "http://api.openweathermap.org/geo/1.0/reverse"
    geo_params = {
        "lat": lat,
        "lon": lon,
        "limit": 5,
        "appid": settings.OPENWEATHER_API_KEY,
    }

    geo_response = requests.get(geo_url, params=geo_params)
    locations = geo_response.json()

    city_name = None

    if locations:
        for loc in locations:
            russian_name = loc.get("local_names", {}).get("ru")
            if russian_name:
                return russian_name
        for loc in locations:
            state = loc.get("state")
            if state:
                return state
        if locations[0].get("name"):
            return locations[0]["name"]

    return city_name if city_name else default
