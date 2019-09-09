"""
buff library
==________==
"""
from logic.models import Role, WakeUpEnum, RoleEnum


def kill(player_buff, player):
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
