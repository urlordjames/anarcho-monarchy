from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginUser, name="login"),
    path("resetpassword/", views.passwordReset, name="password reset"),
    path("logout/", views.logoutUser, name="logout"),
]
