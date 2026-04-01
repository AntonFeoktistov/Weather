from django.shortcuts import render, redirect
from django.views import View


class IndexView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main:home")

        return render(request, "main/index.html")
