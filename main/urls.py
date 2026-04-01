from django.contrib import admin
from django.urls import include, path
from main.views.home_view import HomeView
from main.views.index_view import IndexView
from main.views.log_in_out_view import CustomLoginView, CustomLogoutView
from main.views.register_view import RegisterView
from main.views.add_location_view import AddLocationView
from main.views.delete_location_view import DeleteLocationView
from main.views.refresh_weather import RefreshWeatherView, RefreshWeatherIndexView

app_name = "main"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("home/", HomeView.as_view(), name="home"),
    path("add-location/", AddLocationView.as_view(), name="add_location"),
    path("delete-location/", DeleteLocationView.as_view(), name="delete_location"),
    path("refresh-weather/", RefreshWeatherView.as_view(), name="refresh_weather"),
    path(
        "refresh-index/",
        RefreshWeatherIndexView.as_view(),
        name="refresh_index",
    ),
]
