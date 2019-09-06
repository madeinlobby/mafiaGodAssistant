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
    duration = models.IntegerField()
    type = models.CharField(max_length=200, choices=BuffType.choices())
    priority = models.IntegerField()
    announce = models.BooleanField()
    neutralizer = models.ManyToManyField('self', blank=True)


class Ability(models.Model):
    name = models.CharField(max_length=200)


class Role(models.Model):
    name = models.CharField(max_length=200)
    abilities = models.ManyToManyField(Ability, blank=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # will be god
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField()  # true -> alive   false -> die
    role = models.ForeignKey(Role, blank=True,default=None, on_delete=models.CASCADE)
    buffs = models.ManyToManyField(Buff, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=None)
