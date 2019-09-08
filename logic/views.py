from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MGA.models import Event, User
from logic.models import Role, Game, Player, Duration, RoleEnum, Buff, PlayerBuff
from logic.serializers import RoleSerializer, GameSerializer, PlayerSerializer


@api_view(['GET'])
def get_all_roles(request):
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def random_roles(role_dict, game_id):
    game = Game.objects.get(id=game_id)
    members = game.event.members
    all = 0
    for role in role_dict:
        all += role_dict[role]

    members = members.order_by('?')
    if all == len(members):
        for (member, role) in zip(members, role_dict):
            role_value = role_dict[role]
            if role_value != 0:
                role_dict[role] -= 1
                role_obj = Role.objects.get(id=role)
                Player.objects.create(status=True, user=member, role=role_obj, game=game).save()

        game.save()
        serializer = PlayerSerializer(game.player_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def set_game_role(request):
    game_id = request.data.get('game_id')
    role_dict = request.data.get('role_dict')
    return random_roles(role_dict, game_id)


@api_view(['GET', 'POST'])
def create_game(request):
    try:
        event_id = request.data.get('event_id')
        event = Event.objects.get(id=event_id)
        game = Game.objects.create(owner=event.owner, event=event)
        game.save()

        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def decrease_duration(player):
    for buff in player.buffs.all():
        if buff.duration == Duration.always:
            continue
        buff.player_duration -= 12
        if buff.player_duration < 0:
            buff.delete()


def check_neutralizer(player):  # todo bug delete nadare be nazaret?
    for buff in player.buffs.all():
        for n_buff in buff.neutralizer.all():
            for buffNeu in player.buffs.all():
                if buffNeu.type == n_buff.type:
                    buffNeu.delete()
                    buff.delete()


@api_view(['POST', 'GET'])
def day_to_night(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    players = game.player_set

    for player in players.all():
        if player.status:
            decrease_duration(player)
            check_neutralizer(player)

    return order_awake(game)


@api_view(['POST', 'GET'])
def night_to_day(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    players = game.player_set

    for player in players.all():
        if player.status:
            decrease_duration(player)
            check_neutralizer(player)

    return day_happening(game)


def day_happening(game):
    dictionary = dict()
    players = game.player_set
    for player in players.all():
        for buff in player.buffs.all():
            if buff.announce:
                dictionary.update({player.user.username: buff.type})
    return Response(dictionary)


def order_awake(game):  # todo
    dictionary = dict()
    players = game.player_set

    dictionary.update({str(RoleEnum.mafia): True})

    for player in players.all():
        if str(player.role.name) == str(RoleEnum.doctor):
            dictionary.update({str(RoleEnum.doctor): player.status})

        if str(player.role.name) == str(RoleEnum.detective):
            dictionary.update({str(RoleEnum.detective): player.status})

    return Response(dictionary)


def alive_player(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    players = game.player_set

    alivePlayers = []
    for p in players:
        if p.stauts:
            alivePlayers.append(p.user.username)

    serializer = PlayerSerializer(alivePlayers, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


def make_buff(role, opponent):
    abilities = role.abilities

    for ability in abilities.all():
        buffs = ability.buffs
        for buff in buffs.all():
            player_buff = PlayerBuff.objects.create(duration=buff.duration, type=buff.type,
                                                    priority=buff.priority, announce=buff.announce,
                                                    player_duration=Duration.get_duration_by_duration_name(
                                                        buff.duration).value)
            for n in buff.neutralizer.all():
                player_buff.neutralizer.add(n)
            player_buff.save()
            opponent.buffs.add(player_buff)
            opponent.save()


@api_view(['POST'])
def set_night_aims(request):
    response_dic = dict()
    aims_dic = request.data.get('aim_dic')
    for aim in aims_dic:
        role = Role.objects.get(name=RoleEnum(aim))
        user = User.objects.get(username=aims_dic[aim])
        player = Player.objects.get(user=user)
        if role.name == str(RoleEnum.detective):
            response_dic.update({role.name: player.role.team})
        make_buff(role, player)
    return Response(response_dic)
