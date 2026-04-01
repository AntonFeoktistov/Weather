from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from main.forms import SignUpForm


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
