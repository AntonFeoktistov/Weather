from dataclasses import asdict
from django.utils import timezone
import json

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Location
from django.contrib import messages
from django.shortcuts import redirect

from main.service.weather_finder import WeatherFinder


class AddLocationView(LoginRequiredMixin, View):

    def post(self, request):
        name = request.POST.get("name")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        temperature = request.POST.get("temperature")
        description = request.POST.get("description")
        wind_speed = request.POST.get("wind_speed")

        is_location_already_exists = Location.objects.filter(
            user=request.user, name=name
        ).first()

        if is_location_already_exists:
            messages.warning(request, f'Локация "{name}" уже есть в вашем списке')
        else:
            weather = {
                "temperature": temperature,
                "description": description,
                "wind_speed": wind_speed,
            }
            Location.objects.create(
                user=request.user,
                name=name,
                lat=lat,
                lon=lon,
                weather_data=weather,
                weather_updated_at=timezone.now(),
            )
            messages.success(request, f'Локация "{name}" добавлена')

        return redirect(request.META.get("HTTP_REFERER", "weather"))
