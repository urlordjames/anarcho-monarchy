from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginUser, name="login"),
    path("resetpassword/", views.passwordReset, name="password reset"),
    path("logout/", views.logoutUser, name="logout"),
    path("players/", views.viewAllPlayers, name="player list"),
    path("myplayers/", views.viewUserPlayers, name="user player list"),
    path("createplayer/", views.createPlayer, name="create player"),
    path("editplayer/", views.editPlayer, name="edit player"),
]
