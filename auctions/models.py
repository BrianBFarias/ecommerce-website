# from django.conf import settings
from typing import Any
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import datetime


class User(AbstractUser):
    pass

class Item(models.Model):
    price = models.IntegerField()
    title =  models.CharField(max_length=64)
    category = models.CharField(max_length=32, default='None')
    description = models.CharField(max_length=100*20)
    time = models.DateTimeField(default=now, editable=False)
    image = models.URLField(default='https://media.istockphoto.com/id/1055079680/vector/black-linear-photo-camera-like-no-image-available.jpg?s=612x612&w=0&k=20&c=P1DebpeMIAtXj_ZbVsKVvg-duuL0v9DlrOZUvPG6UJk=')
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    time = models.DateTimeField(default=now, editable=False)
    def __str__(self):
        return f"'{self.message}' ~ {self.user}"


class Item_Message_Group(models.Model):
    messages = models.ManyToManyField(Message, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, default=False)
    def __str__(self):
        return f"{self.item}"

class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.item}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchlist = models.ManyToManyField(Item, blank=True)
    def __str__(self):
       return f"{self.user}'s WatchList"
