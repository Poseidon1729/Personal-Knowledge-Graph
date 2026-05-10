from django.urls import path
from .views import users_list, user_login, signup

urlpatterns = [
    path("user_list/", users_list, name="user_list"),
    path("login/", user_login, name="login"),
    path("logout/", user_login, name="logout"),
    path("signup/", signup, name="signup"),
]
