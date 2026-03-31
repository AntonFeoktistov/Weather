from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from main.geoloc import get_location_coords
from main.weather import get_weather_by_coords
from .forms import LocationSearchForm, SignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main:home")

        return render(request, "main/index.html")


class RegisterView(View):

    template_name = "main/register.html"
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("main:home")
        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):

    template_name = "main/login.html"
    redirect_authenticated_user = True
    next_page = "main:home"


class CustomLogoutView(LogoutView):
    next_page = "main:home"


class HomeView(LoginRequiredMixin, View):
    template_name = "main/home.html"
    login_url = "main:login"
    redirect_field_name = "next"

    def get(self, request):
        search_form = LocationSearchForm()
        return render(
            request,
            self.template_name,
            {
                "search_form": search_form,
            },
        )

    def post(self, request):
        search_form = LocationSearchForm(request.POST)

        if search_form.is_valid():
            location_request = search_form.cleaned_data["query"]
            request.session["last_search"] = location_request
            location = get_location_coords(location_request)
            if location:
                print(location)
                weather = get_weather_by_coords(location.lat, location.long)
                print(weather)
                if weather:
                    return render(
                        request,
                        self.template_name,
                        {
                            "search_form": search_form,
                            "query": location_request,
                            "weather": weather,
                        },
                    )
        return render(
            request,
            self.template_name,
            {"search_form": search_form, "error_message": "Погода не найдена"},
        )
