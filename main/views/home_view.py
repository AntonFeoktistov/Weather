from dataclasses import asdict

from django.shortcuts import render, redirect
from django.views import View
from main.service.errors import WeatherNotFoundError
from main.service.weather_finder import WeatherFinder
from main.forms import LocationSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(LoginRequiredMixin, View):
    template_name = "main/home.html"
    login_url = "main:login"
    redirect_field_name = "next"

    def __init__(self):
        self.weather_finder = WeatherFinder()

    def get(self, request):
        locations = request.user.locations.all()
        print(locations)
        search_form = LocationSearchForm()
        return render(
            request,
            self.template_name,
            {
                "search_form": search_form,
                "query": request.session.get("last_query", ""),
                "weather": request.session.get("last_weather", ""),
                "locations": locations,
            },
        )

    def post(self, request):
        search_form = LocationSearchForm(request.POST)

        if search_form.is_valid():
            location_request = search_form.cleaned_data["query"]
            request.session["last_query"] = location_request
            locations = request.user.locations.all()
            try:
                weather = self.weather_finder.get_weather_by_city_name(location_request)
                request.session["last_weather"] = asdict(weather)
                print(weather)
                return render(
                    request,
                    self.template_name,
                    {
                        "search_form": search_form,
                        "query": location_request,
                        "weather": weather,
                        "locations": locations,
                    },
                )
            except WeatherNotFoundError:
                return render(
                    request,
                    self.template_name,
                    {
                        "search_form": search_form,
                        "error_message": "Погода не найдена",
                        "locations": locations,
                    },
                )
