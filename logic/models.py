from enum import Enum

from django.db import models

from MGA.models import User, Event


class Duration(Enum):
    H24 = 24
    H48 = 48
    H12 = 12
    always = 10000000

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_duration_by_duration_name(cls, duration):
        for i in cls:
            if str(i) == duration:
                return Duration(i.value)
        return None


class BuffType(Enum):
    Kill = 'kill'
    Save = 'save'
    NotChange = 'در امان'
    Silent = 'سکوت'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Buff(models.Model):
    duration = models.CharField(max_length=200, choices=Duration.choices())
    type = models.CharField(max_length=200, choices=BuffType.choices())
    priority = models.IntegerField()
    announce = models.BooleanField()
    neutralizer = models.ManyToManyField('self', blank=True)
    function_name = models.CharField(max_length=250, default=None, null=True)


class PlayerBuff(Buff):
    player_duration = models.IntegerField()


class AbilityEnum(Enum):
    can_save = 'نجات'
    can_ask = 'پرسش نقش'
    can_kil = 'کشتن فرد'
    can_jail = 'زندانی کردن'
    can_silence = 'ساکت کردن'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Ability(models.Model):
    name = models.CharField(max_length=200)
    buffs = models.ManyToManyField(Buff, related_name='ability_buff')


class RoleEnum(Enum):
    citizen = 'شهروند عادی'
    doctor = 'دکتر'
    detective = 'کارآگاه'
    mafia = 'مافیا'
    jailer = 'زندانبان'
    dentist = 'دندان پزشک'
    surgeon = 'جراح'
    mayor = 'شهردار'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    def __str__(self):
        return self.value


class TeamEnum(Enum):
    mafia = 'مافیا'
    citizen = 'شهروندان'
    independence = 'مستقل'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    def __str__(self):
        return 'تیم ' + self.value


class Role(models.Model):
    name = models.CharField(max_length=200, choices=RoleEnum.choices())
    abilities = models.ManyToManyField(Ability, blank=True)
    team = models.CharField(max_length=50, choices=TeamEnum.choices(), default=None)
    limit = models.IntegerField(default=100000, blank=True, null=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # will be god
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField()  # true -> alive   false -> die
    role = models.ForeignKey(Role, blank=True, default=None, on_delete=models.CASCADE)
    buffs = models.ManyToManyField(PlayerBuff, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, default=None)
    limit = models.IntegerField(default=100000, blank=True, null=True)

    def __str__(self):
        return self.user.username
