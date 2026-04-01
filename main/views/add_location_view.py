from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Location
from django.contrib import messages
from django.shortcuts import redirect


class AddLocationView(LoginRequiredMixin, View):

    def post(self, request):
        name = request.POST.get("name")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")

        is_location_already_exists = Location.objects.filter(
            user=request.user, name=name
        ).first()

        if is_location_already_exists:
            messages.warning(request, f'Локация "{name}" уже есть в вашем списке')
        else:
            Location.objects.create(user=request.user, name=name, lat=lat, lon=lon)
            messages.success(request, f'Локация "{name}" добавлена')

        return redirect(request.META.get("HTTP_REFERER", "weather"))
