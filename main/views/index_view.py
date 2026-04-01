from django.shortcuts import render, redirect
from django.views import View

from main.models import Location


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main:home")

        all_locations = Location.objects.all().order_by("-id")
        locations = self._find_unick_locations(all_locations)
        return render(request, "main/index.html", {"locations": locations})

    def _find_unick_locations(self, locations: list, max_count=5):
        unique_locations = []
        seen = set()
        for location in locations:
            if location.name not in seen:
                seen.add(location.name)
                unique_locations.append(location)
            if len(unique_locations) >= max_count:
                break
        return unique_locations
