from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path("login/", views.login_request, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout_request, name="logout"),
    path("delete/<username>", views.delete_request, name='delete'),
    path('', views.home_page, name="home")
]