import time
import requests
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password, ValidationError
from .models import Player, Nation, Law

def index(request):
    user = request.user
    accounts = 0
    nation = None
    if user.is_authenticated:
        accounts = len(Player.objects.all().filter(owner=user))
        nation = Nation.objects.get(owner=user)
    return render(request, "index.html", {"username": user.get_username(),
                                          "noaccount": accounts == 0,
                                          "hasnation": not nation is None})
@csrf_protect
def loginUser(request):
    if request.method == "GET":
        return render(request, "login.html")
    elif request.method == "POST":
        formdata = request.POST
        user = authenticate(request, username=formdata["username"], password=formdata["password"])
        if user is None:
            messages.error(request, "authentication failed")
            return redirect("/login/")
        else:
            login(request, user)
            messages.success(request, "you have successfully logged in!")
            return redirect("/")
    else:
        return HttpResponse(status=405)

@csrf_protect
def passwordReset(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "GET":
            return render(request, "passwordreset.html")
        elif request.method == "POST":
            if not user.check_password(request.POST["oldpassword"]):
                messages.error(request, "old password incorrect")
                return redirect("/resetpassword/")
            password = request.POST["password"]
            try:
                validate_password(password)
            except ValidationError as errors:
                for error in errors:
                    messages.error(request, error)
                return redirect("/resetpassword/")
            user.set_password(password)
            user.save()
            messages.success(request, "password changed")
            return redirect("/")  
        else:
            return HttpResponse(status=405)
    else:
        messages.error(request, "you are not logged in")
        return redirect("/login/")

def logoutUser(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect("/")

def viewAllPlayers(request):
    return render(request, "allplayerlist.html", {"title": "Player List",
                                                  "list": Player.objects.all()})
def viewUserPlayers(request):
    user = request.user
    if user.is_authenticated:
        return render(request, "playerlist.html", {"title": "Your Players",
                                                   "list": Player.objects.all().filter(owner=user)})
    else:
        return HttpResponse(status=401)

@csrf_protect
def createPlayer(request):
    user = request.user
    if not user.is_authenticated:
        return HttpRespose(status=401)
    if request.method == "GET":
        return render(request, "createplayer.html")
    elif request.method == "POST":
        if not user.is_superuser and len(Player.objects.all().filter(owner=user)) >= 3:
            messages.error(request, "player limit exceeded, if you need to register more players contact me")
            return redirect("/myplayers/")
        username = request.POST["username"]
        r = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?at={int(time.time())}")
        if r.status_code != 200:
            messages.error(request, "unable to fetch UUID (account nonexistent or Mojang API down)")
            return redirect("/createplayer/")
        response = r.json()
        newplayer = Player(owner=user, uuid=response["id"], nation=None)
        try:
            newplayer.full_clean()
            newplayer.save()
        except ValidationError as e:
            for i in e:
                messages.error(request, i)
            return redirect("/createplayer/")
        messages.success(request, "account registered successfully")
        return redirect("/myplayers/")
    else:
        return HttpResponse(status=405)

@csrf_protect
def editPlayer(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(status=401)
    player = get_object_or_404(Player, uuid=request.GET.get("uuid"))
    if player.owner != user:
        return HttpResponse(status=403)
    if request.method == "GET":
        return render(request, "editplayer.html", {"nations": Nation.objects.all()})
    elif request.method == "POST":
        requestednation = request.POST.get("nation")
        nation = None
        if not requestednation is None and requestednation != "":
            nation = get_object_or_404(Nation, name=request.POST.get("nation"))
        player.nation = nation
        player.save()
        messages.success(request, "player alliance set successfully")
        return redirect("/myplayers/")
    else:
        return HttpResponse(status=405)

def viewNations(request):
    return render(request, "nationlist.html", {"title": "Nation List",
                                               "list": Nation.objects.all()})
@csrf_protect
def createNation(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(status=401)
    if request.method == "GET":
        return render(request, "createnation.html")
    elif request.method == "POST":
        if not user.is_superuser and len(Nation.objects.all().filter(owner=user)) >= 1:
            messages.error(request, "you may only lead one nation")
            return redirect("/")
        newnation = Nation(owner=user, name=request.POST.get("name"), about=request.POST.get("about"))
        try:
            newnation.full_clean()
            newnation.save()
        except ValidationError as e:
            for i in e:
                messages.error(request, i)
            return redirect("/createnation/")
        messages.success(request, "nation created successfully")
        return redirect("/nations/")
    else:
        return HttpResponse(status=405)

def nationInfo(request):
    nation = get_object_or_404(Nation, name=request.GET.get("nation"))
    return render(request, "nationinfo.html", {"nation": nation,
                                               "laws": Law.objects.all().filter(nation=nation),
                                               "members": Player.objects.all().filter(nation=nation)})

@csrf_protect
def editNation(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(status=401)
    nation = get_object_or_404(Nation, owner=user)
    if nation.owner != user:
        return HttpResponse(status=403)
    if request.method == "GET":
        return render(request, "editnation.html", {"nation": nation,
                                                   "laws": Law.objects.all().filter(nation=nation)})
    elif request.method == "POST":
        try:
            nation.about = request.POST.get("about")
            nation.full_clean()
            nation.save()
        except ValidationError as e:
            for i in e:
                messages.error(request, i)
            return redirect("/createnation/")
        messages.success(request, "nation created successfully")
        return redirect("/editnation/")
    else:
        return HttpResponse(status=405)

@csrf_protect
def createLaw(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(status=401)
    nation = get_object_or_404(Nation, name=request.POST.get("nation"))
    if nation.owner != user:
        return HttpResponse(status=403)
    newlaw = Law(nation=nation)
    try:
        newlaw.full_clean()
        newlaw.save()
    except ValidationError as e:
        for i in e:
            messages.error(request, i)
    messages.success(request, "law successfully created")
    return redirect("/editnation/")

@csrf_protect
def editLaw(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(status=401)
    law = get_object_or_404(Law, pk=request.POST.get("id"))
    nation = law.nation
    if nation.owner != user:
        return HttpResponse(status=403)
    law.text = request.POST.get("content")
    try:
        law.full_clean()
        law.save()
    except ValidationError as e:
        for i in e:
            messages.error(request, i)
    messages.success(request, "law successfully edited")
    return redirect("/editnation/")

@csrf_protect
def deleteLaw(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponse(status=401)
    law = get_object_or_404(Law, pk=request.POST.get("id"))
    nation = law.nation
    if nation.owner != user:
        return HttpResponse(status=403)
    law.delete()
    messages.success(request, "law successfully deleted")
    return redirect("/editnation/")
