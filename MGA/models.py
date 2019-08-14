from django.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=16)
    bio = models.CharField(max_length=250)
    phoneNumber = models.BigIntegerField()
    city = models.CharField(max_length=200)
    email = models.EmailField()
    confirm = models.BooleanField(default=False)
