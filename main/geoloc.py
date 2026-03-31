import requests
import time
import logging
from requests.exceptions import RequestException, Timeout, ConnectionError
from django.conf import settings
from django.core.cache import cache
from .dto import LocationDto

logger = logging.getLogger(__name__)


def get_location_coords(city_name, retries=3):
    for attempt in range(retries):
        try:
            location_dto = geocode_city(city_name)
            return location_dto
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return


def geocode_city(city_name):

    url = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": settings.YANDEX_GEOCODER_API_KEY,
        "geocode": city_name,
        "lang": "en_US",
        "format": "json",
        "results": 1,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        found = int(
            data["response"]["GeoObjectCollection"]["metaDataProperty"][
                "GeocoderResponseMetaData"
            ]["found"]
        )
        if found == 0:
            logger.info(f"Город '{city_name}' не найден в Yandex Geocoder")
            return None

        # TODO сделать валидатор который предупреждает что запрос плохой и локация нерелевантна

        geo_object = data["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"
        ]

        pos = geo_object["Point"]["pos"]
        lon, lat = pos.split()

        lat = round(float(lat), 2)
        lon = round(float(lon), 2)
        print("rrr", lat, lon)
        result = {
            "lat": lat,
            "lon": lon,
            "full_name": geo_object["name"],
        }
        return make_location_dto(result)

    except requests.exceptions.Timeout:
        logger.error(f"Таймаут при запросе к Yandex Geocoder для города: {city_name}")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса к Yandex Geocoder: {e}")
        return None
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        return None


# result = {"lat": float(lat), "lon": float(lon), "full_name": full_name}
def make_location_dto(data: dict) -> LocationDto:
    name = data.get("full_name", "")
    long = data.get("lon", 0)
    lat = data.get("lat", 0)
    return LocationDto(name=name, long=long, lat=lat)


def select_best_geo_object(features: list):

    best_result = None
    best_priority = 999

    for feature in features:
        geo_object = feature["GeoObject"]

        meta_data = geo_object.get("metaDataProperty", {})
        geocoder_meta = meta_data.get("GeocoderMetaData", {})
        kind = geocoder_meta.get("kind", "")

        if kind in IGNORED_KINDS:
            logger.debug(f"Игнорируем объект: {geo_object.get('name')} (kind={kind})")
            continue

        if kind in OBJECT_PRIORITY:
            current_priority = OBJECT_PRIORITY[kind]

            if current_priority < best_priority:
                best_priority = current_priority
                best_result = {
                    "geo_object": geo_object,
                    "kind": kind,
                    "priority": current_priority,
                }

    return best_result


def extract_location_data(geo_object: dict) -> dict:

    pos = geo_object["Point"]["pos"]
    lon, lat = pos.split()

    return {
        "lat": float(lat),
        "lon": float(lon),
        "full_name": geo_object.get("name", ""),
    }


OBJECT_PRIORITY = {
    "locality": 1,
    "district": 2,
    "province": 3,
}

IGNORED_KINDS = {
    "street",
    "house",
    "metro",
    "railway_station",
    "airport",
    "park",
    "attraction",
    "hydro",
}
