from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Location
from django.contrib import messages
from django.shortcuts import redirect


class DeleteLocationView(LoginRequiredMixin, View):

    def post(self, request):
        name = request.POST.get("name")

        if name:
            deleted_count, _ = Location.objects.filter(
                user=request.user, name=name
            ).delete()

            if deleted_count:
                messages.success(request, f'Локация "{name}" удалена из избранного')
            else:
                messages.warning(request, f'Локация "{name}" не найдена')

        return redirect(request.META.get("HTTP_REFERER", "main:home"))
