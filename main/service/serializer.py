from main.dto import LocationDto, WeatherDto


class Serializer:
    def make_location_dto(self, data: dict) -> LocationDto:
        name_en = data.get("name_en", "")
        name_ru = data.get("name_ru", "")
        state = data.get("state", "")
        lon = data.get("lon", 0)
        lat = data.get("lat", 0)
        return LocationDto(
            name_en=name_en, name_ru=name_ru, state=state, lon=lon, lat=lat
        )

    def make_weather_dto(self, data: str) -> WeatherDto:
        location = data.get("location", "")
        temperature = data.get("temperature", 0)
        description = data.get("description", "")
        wind_speed = data.get("wind_speed", 0)
        return WeatherDto(
            location=location,
            temperature=temperature,
            description=description,
            wind_speed=wind_speed,
        )
