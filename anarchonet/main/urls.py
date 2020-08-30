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
    path("nations/", views.viewNations, name="nation list"),
    path("createnation/", views.createNation, name="create nation"),
    path("editnation/", views.editNation, name="edit nation"),
    path("nationinfo/", views.nationInfo, name="nation info"),
    path("createlaw/", views.createLaw, name="create law"),
    path("editlaw/", views.editLaw, name="edit law"),
]
