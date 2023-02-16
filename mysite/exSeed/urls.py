from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from . import views


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup", views.signup, name="signup"),
    path('', TemplateView.as_view(template_name="home.html"), name="home")
]