from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Player

def index(request):
    user = request.user
    accounts = 0
    if user.is_authenticated:
        accounts = len(Player.objects.all().filter(owner=user))
    return render(request, "index.html", {"username": user.get_username(),
                                          "hasaccount": accounts != 0})
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
    return render(request, "basiclist.html", {"title": "Player List",
                                              "listof": "Players",
                                              "list": Player.objects.all()})
