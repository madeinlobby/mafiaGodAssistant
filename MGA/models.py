import jwt
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.manager import BaseManager
from django.utils import timezone


class UserManager(BaseManager):
    def create_user(self, name, username, password, bio, phoneNumber, city, email):
        user = User(name=name, username=username, bio=bio, phoneNumber=phoneNumber, city=city,
                    email=email)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    bio = models.CharField(max_length=250, blank=True, null=True)
    phoneNumber = models.BigIntegerField()
    city = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField()
    confirm = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'username', 'password', 'bio', 'phoneNumber', 'city', 'email']

    def __str__(self):
        return self.username


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
    admins = models.ManyToManyField(User, related_name='admins')  # todo + bydefault creator needs to be admin
