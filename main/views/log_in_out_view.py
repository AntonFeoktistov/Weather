from django.contrib.auth.views import LoginView, LogoutView


class CustomLoginView(LoginView):

    template_name = "main/login.html"
    redirect_authenticated_user = True
    next_page = "main:home"


class CustomLogoutView(LogoutView):
    next_page = "main:home"
