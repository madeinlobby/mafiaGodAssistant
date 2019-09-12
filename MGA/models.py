from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings
# from pushy.models import Device


class Token(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Rate(models.Model):
    number_of_votes = models.IntegerField()
    mean_score = models.IntegerField(default=0)


class UserManager(BaseUserManager):
    def create_user(self, name, username, password, bio, phoneNumber, city, email):
        user = User(name=name, username=username, bio=bio, phoneNumber=phoneNumber, city=city,
                    email=email)
        user.set_password(password)
        user.save()
        user.is_staff = True
        return user

    def create_superuser(self, name, username, password, bio, phoneNumber, city, email):
        user = self.create_user(name, username, password, bio, phoneNumber, city, email)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    name = models.CharField(max_length=200)
    bio = models.CharField(max_length=250, blank=True, null=True)
    phoneNumber = models.BigIntegerField()
    city = models.CharField(max_length=200, blank=True, null=True)
    confirm = models.BooleanField(default=False, blank=True, null=True)
    rate = models.OneToOneField(Rate, related_name='u_rate', on_delete=models.CASCADE, blank=True, null=True)
    # user_device = models.OneToOneField(Device, on_delete=models.CASCADE, default=None, blank=True, null=True,
    #                                    related_name='user_device')

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'password', 'bio', 'phoneNumber', 'city', 'email']

    def __str__(self):
        return self.username


class Organization(models.Model):
    name = models.CharField(max_length=200, default='untitled')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    admins = models.ManyToManyField(User, related_name='admins',
                                    default=None, through='AdminShip')  # todo + by default creator needs to be admin


class AdminShip(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class Event(models.Model):
    # location todo
    date = models.DateTimeField(default=timezone.now)
    capacity = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    members = models.ManyToManyField(User, related_name='members',
                                     through='MemberShip')  # todo
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True, null=True)
    private = models.BooleanField(default=False)
    xlat = models.FloatField(null=True)
    ylat = models.FloatField(null=True)
    organization = models.ForeignKey(Organization, related_name='organization', default=None, on_delete=models.CASCADE)


class MemberShip(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Reason(models.Model):
    text = models.CharField(max_length=300)

    def __str__(self):
        return self.text


class Report(models.Model):
    r_reason = models.ManyToManyField(Reason, related_name='r_reason', through='ReportShip')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ReportShip(models.Model):
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)


class Ban(models.Model):
    b_reason = models.ManyToManyField(Reason, related_name='b_reason')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, default=None)


class BanShip(models.Model):
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    ban = models.ForeignKey(Ban, on_delete=models.CASCADE)


class Friend(models.Model):
    user = models.ForeignKey(User, related_name='friend_user', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)


class Notification(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', default=None)
    text = models.TextField()
    time = models.DateTimeField()
    read = models.BooleanField(default=False)


class Cafe(models.Model):
    name = models.CharField(max_length=200)
    phoneNumber = models.BigIntegerField()
    telephone = models.BigIntegerField()
    capacity = models.IntegerField()
    rate = models.OneToOneField(Rate, related_name='c_rate', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    forbiddens = models.TextField()
    # location
