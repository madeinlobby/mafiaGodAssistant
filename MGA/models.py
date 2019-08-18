from django.db import models
# from django.contrib.auth.models import User
from django.utils import timezone


# from rest_framework_jwt.serializers import User
# from django.contrib.gis.db import models


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=16)
    bio = models.CharField(max_length=250, blank=True, null=True)
    phoneNumber = models.BigIntegerField()
    city = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    confirm = models.BooleanField(default=False)
    # location = models.PointField()


# azash inherih mikonam yadam bashe!

class Event(models.Model):
    # location todo
    date = models.DateTimeField(default=timezone.now)
    capacity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    # event ?
    members = models.ManyToManyField(User, blank=True, related_name='members')  # todo
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True, null=True)


class Organization(models.Model):
    name = models.CharField(max_length=200, default='untitled')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    admins = models.ManyToManyField(User, related_name='admins')  # todo + by default creator needs to be admin
