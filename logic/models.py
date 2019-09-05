from enum import Enum

from django.db import models

from MGA.models import User, Event


class Duration(Enum):
    OneDay = 'one day'
    OneNight = 'one night'
    H24 = '24 hours'
    H48 = '48 hours'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class BuffType(Enum):
    Kill = 'kill'
    Save = 'save'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Buff(models.Model):
    duration = models.CharField(max_length=200, choices=Duration.choices())
    type = models.CharField(max_length=200, choices=BuffType.choices())
    priority = models.IntegerField()
    announce = models.BooleanField()
    neutralizer = models.ManyToManyField('self', blank=True, null=True)


class Ability(models.Model):
    name = models.CharField(max_length=200)


class Role(models.Model):
    name = models.CharField(max_length=200)
    abilities = models.ManyToManyField(Ability,blank=True, null=True)


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField()
    role = models.ManyToManyField(Role)
    buffs = models.ManyToManyField(Buff)


class Game(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # will be god
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
