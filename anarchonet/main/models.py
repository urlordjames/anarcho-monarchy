import requests
from django.contrib.auth.models import User
from django.db import models

def isRealUUID(uuid):
    r = requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names")
    if r.status_code != 200:
        raise ValidationError("invalid UUID passed to Player model")

class Nation(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    about = models.CharField(max_length=500, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")

    def __str__(self):
        return self.name

class Law(models.Model):
    text = models.CharField(max_length=200, null=False, blank=False)
    nation = models.ForeignKey(Nation, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Player(models.Model):
    uuid = models.CharField(max_length=32, null=False, blank=False, unique=True, validators=[isRealUUID])
    nation = models.ForeignKey(Nation, null=True, blank=True, on_delete=models.SET_NULL)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        r = requests.get(f"https://api.mojang.com/user/profiles/{self.uuid}/names")
        return r.json()[-1]["name"]
