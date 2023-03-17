from django.urls import path, include
from . import views

"""
List of the urls in the website and linking them to their views
"""
urlpatterns = [
    path("login/", views.login_request, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout_request, name="logout"),
    path("delete/<username>", views.delete_request, name='delete'),
    path('', views.home_page, name="home"),
    path("leaderboard", views.leaderboard, name="leaderboard"),  # Refers to the leaderboard view when
    # exseed.duckdns.org/leaderboard is received
    path("compass", views.compass, name="compass"),
    path("profile", views.profile_page, name="profile"),
    path("change_profile_picture", views.change_profile_picture, name ="change_profile_picture"),
    path("graph", views.graph, name="graph_test"),
    path("addScore", views.addScore, name="score"),
    path("change_title/<title>", views.change_title, name="change_title")
]