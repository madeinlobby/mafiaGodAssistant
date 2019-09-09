from enum import Enum

from django.db import models

from MGA.models import User, Event


class WakeUpEnum(Enum):
    every_night = 0
    every_one_night = 1
    every_two_night = 2
    every_three_night = 3
    every_five_night = 5

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def get_wakeUpEnum_by_wake_up_name(cls, wake_up):
        for i in cls:
            if str(i) == wake_up:
                return WakeUpEnum(i.value)
        return None


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
    NotChange_announce = 'در امان(خارج از بازی)'
    Silent = 'سکوت'
    NotChange = 'در امان(داخل از بازی)'
    SendRole = 'ارسال نقش'
    Save_at_night = 'نمردن در شب'
    Make_citizen = 'تبدیل به شهروند عادی'
    Make_alive = 'زنده کردن'
    One_shot_alive = 'یکبار سیو در مقابل گلوله'

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
    put_player_role = models.CharField(max_length=200, blank=True, null=True, default='none')


class AbilityEnum(Enum):
    can_save = 'نجات'
    can_ask = 'پرسش نقش'
    can_kil = 'کشتن فرد'
    can_jail = 'زندانی کردن'
    can_silence = 'ساکت کردن'
    can_protect = 'محافظت کردن'
    can_send_role = 'ارسال نقش'
    can_save_at_night = 'زنده ماندن در شب'
    can_change_role_to_citizen = 'تبدیل به شهروند عادی'
    reverse_inquiry = 'استعلام برعکس'
    can_alive = 'زنده کردن'
    one_shot_alive = 'یکبار سیو شدن در برابر گلوله'

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
    hero = 'قهرمان'
    wolfman = 'گرگ نما'
    simin = 'سیمین'
    priest = 'کشیش'
    grave_digger = 'گورکن'
    insincere = 'دورو'
    jesus = 'عیسی'
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
    werewolf = 'گرگینه ها'

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
    wake_up = models.CharField(max_length=250, default=0, blank=True, null=True, choices=WakeUpEnum.choices())
    own_buffs = models.ManyToManyField(Buff, blank=True)

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
    wake_up_limit = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.user.username
