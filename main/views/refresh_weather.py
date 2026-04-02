from dataclasses import asdict
from django.utils import timezone
import json

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Location
from django.contrib import messages
from django.shortcuts import redirect

from main.service.weather_finder import WeatherFinder


class RefreshWeatherView(LoginRequiredMixin, View):

    def post(self, request):
        locations = Location.objects.filter(user=request.user)

        refresher = Refresher()
        refresher._refresh_weather(request, locations)

        return redirect(request.META.get("HTTP_REFERER", "main:home"))


class RefreshWeatherIndexView(View):

    def post(self, request):
        locations = []
        location_ids = request.POST.getlist("location_ids")
        for location_id in location_ids:
            location = Location.objects.get(id=location_id)
            locations.append(location)
        refresher = Refresher()
        refresher._refresh_weather(request, locations)

        return redirect(request.META.get("HTTP_REFERER", "main:index"))


class Refresher:
    def _refresh_weather(self, request, locations: list):
        try:
            weather_finder = WeatherFinder()
            for location in locations:
                weather_dto = weather_finder.get_weather_by_city_name(location.name)

                if weather_dto:
                    weather_data = {
                        "temperature": weather_dto.temperature,
                        "description": weather_dto.description,
                        "wind_speed": weather_dto.wind_speed,
                    }
                    location.weather_data = weather_data
                    location.weather_updated_at = timezone.now()
                    location.save()
        except:
            messages.error(
                request, f"Превышен лимит запросов, обновление временно недоступно"
            )
