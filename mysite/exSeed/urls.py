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
    path("leaderboard", views.leaderboard, name="leaderboard"), 
    path("profile", views.profile_page, name ="profile"),
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    path("compass", views.compass, name="compass"),
    path("change_profile_picture", views.change_profile_picture, name ="change_profile_picture")
]
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
=======
    path("compass", views.compass, name="compass")
]
>>>>>>> Stashed changes
