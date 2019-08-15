from django.db import models
from django.conf import settings
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=16)
    bio = models.CharField(max_length=250)
    phoneNumber = models.BigIntegerField()
    city = models.CharField(max_length=200)
    email = models.EmailField()
    confirm = models.BooleanField(default=False)


class Event(models.Model):
    # location todo
    date = models.DateTimeField(default=timezone.now)
    capacity = models.IntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # event ?
    # members todo
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)


class Organization(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # admins todo

