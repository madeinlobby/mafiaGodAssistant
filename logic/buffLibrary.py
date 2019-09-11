"""
buff library
==________==
"""
from logic.models import Role, WakeUpEnum, RoleEnum, PlayerBuff, Buff, BuffType, Duration, Player

not_dead_list_at_night = [RoleEnum.wolfman.value, RoleEnum.half_breed.value, RoleEnum.emotional.value]


def kill(player_buff, player):
    if player.role.name in not_dead_list_at_night:
        player_buff.delete()
        return player

    for buff in player.buffs:
        if buff.type == BuffType.Reverse_kill and buff.put_player_role == player_buff.put_player_role:
            game = player.game
            players = game.player_set
            for player in players:
                if player.role.name == player_buff.put_player_role:
                    player.status = False
                    return

    player.status = False
    player.save()
    print(player)
    print(player.status)
    return player


def send_role(player_buff, player):
    role_name = player_buff.put_player_role
    role_obj = Role.objects.get(name=role_name)
    player.role = role_obj
    player.limit = role_obj.limit
    player.wake_up_limit = WakeUpEnum.get_wakeUpEnum_by_wake_up_name(
        role_obj.wake_up).value
    player.save()


def make_citizen(player_buff, player):  # wolfman ->citizen
    if player.role.name == str(RoleEnum.wolfman):
        role_obj = Role.objects.get(name=str(RoleEnum.citizen.value))
        player.role = role_obj
        player.limit = role_obj.limit
        player.wake_up_limit = WakeUpEnum.get_wakeUpEnum_by_wake_up_name(
            role_obj.wake_up).value
        player.save()


def make_alive(player_buff, player):
    player.status = True
    buff = Buff.objects.get(type=str(BuffType.Silent.value))
    player_buff = PlayerBuff.objects.create(duration=buff.duration, type=buff.type,
                                            priority=buff.priority, announce=buff.announce,
                                            function_name=buff.function_name,
                                            put_player_role=player_buff.put_player_role,
                                            player_duration=Duration.get_duration_by_duration_name(
                                                buff.duration).value)
    player_buff.save()
    player.buffs.add(player_buff)
    player.save()


def make_simple_mafia(player_buff, player):
    role_obj = Role.objects.get(name=RoleEnum.mafia.value)
    player = Player.objects.create(status=True, user=player.user, role=role_obj, game=player.game,
                                   limit=role_obj.limit,
                                   wake_up_limit=WakeUpEnum.get_wakeUpEnum_by_wake_up_name(
                                       role_obj.wake_up).value)
    player.save()
