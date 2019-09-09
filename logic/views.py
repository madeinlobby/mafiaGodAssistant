import itertools

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MGA.models import Event, User
from logic import buffLibrary
from logic.models import Role, Game, Player, Duration, RoleEnum, Buff, PlayerBuff, TeamEnum, BuffType
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
    role_list = list()
    for role in role_dict:
        for x in range(role_dict[role]):
            role_list.append(role)
            all += 1

    members = members.order_by('?')
    if all == len(members):
        for (member, role) in zip(members, role_list):
            role_obj = Role.objects.get(id=role)
            Player.objects.create(status=True, user=member, role=role_obj, game=game,
                                  limit=role_obj.limit).save()
        game.save()
        dic = dict()
        for player in game.player_set.all():
            dic.update({player.user.username: str(player.role)})
        # serializer = PlayerSerializer(game.player_set, many=True)
        return Response(dic, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def speech_for_start_game(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    players = game.player_set
    dic = dict()
    have_mayor = False
    for player in players.all():
        if player.role.name == str(RoleEnum.mayor):
            have_mayor = True
        if player.role.name == str(RoleEnum.surgeon) or player.role.name == str(RoleEnum.doctor):
            dic.update({player.role.name: 'دست ها را بالا بیاورید تا شهردار ببیند'})

    if have_mayor:
        return Response(dic)
    return Response()


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
        buff.save()
        if buff.player_duration <= 0:
            buff.delete()


def check_neutralizer(player):  # todo bug delete nadare be nazaret?
    for buff in player.buffs.all():
        for n_buff in buff.neutralizer.all():
            for buffNeu in player.buffs.all():
                if buffNeu.type == n_buff.type:
                    buffNeu.delete()
                    buff.delete()


def set_buff_effect(player):
    for buff in player.buffs.all():
        if buff.function_name:
            method_to_call = getattr(buffLibrary, buff.function_name)
            method_to_call(player)


@api_view(['POST', 'GET'])
def day_to_night(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    players = game.player_set

    for player in players.all():
        if player.status:
            decrease_duration(player)
            check_neutralizer(player)
            set_buff_effect(player)

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
            set_buff_effect(player)

    end = end_game(game)
    if not end:
        return day_happening(game)
    return Response(end)


def day_happening(game):
    dictionary = dict()
    players = game.player_set
    for player in players.all():
        for buff in player.buffs.all():
            if buff.announce:
                dictionary.update({player.user.username: buff.type})
    return Response(dictionary)


def limited_role_awake(player, dictionary, role_name):
    if str(player.role.name) == str(role_name):
        if player.limit == 0:
            dictionary.update({str(role_name): 'limited'})
        else:
            dictionary.update({str(role_name): player.status})


def role_awake(player, dictionary, role_name):
    if str(player.role.name) == str(role_name):
        dictionary.update({str(role_name): player.status})


def order_awake(game):  # todo
    dictionary = dict()
    players = game.player_set

    dictionary.update({str(RoleEnum.mafia): True})

    for player in players.all():

        role_awake(player, dictionary, RoleEnum.doctor)

        role_awake(player, dictionary, RoleEnum.detective)

        limited_role_awake(player, dictionary, RoleEnum.jailer)

        limited_role_awake(player, dictionary, RoleEnum.surgeon)

        limited_role_awake(player, dictionary, RoleEnum.dentist)

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


def can_put_buff(player):
    for ability in player.role.abilities.all():
        for buff in ability.buffs.all():
            if str(buff.type) == str(BuffType.NotChange):
                return False
    return True


def make_buff(role, opponent):
    if can_put_buff(opponent):
        abilities = role.abilities

        for ability in abilities.all():
            buffs = ability.buffs
            for buff in buffs.all():
                player_buff = PlayerBuff.objects.create(duration=buff.duration, type=buff.type,
                                                        priority=buff.priority, announce=buff.announce,
                                                        function_name=buff.function_name,
                                                        player_duration=Duration.get_duration_by_duration_name(
                                                            buff.duration).value)
                for n in buff.neutralizer.all():
                    player_buff.neutralizer.add(n)
                player_buff.save()
                opponent.buffs.add(player_buff)
                opponent.save()


def decrease_limit(role, game):
    players = game.player_set
    for player in players.all():
        if str(player.role.name) == str(role.name):
            player.limit -= 1
            player.save()
            return


@api_view(['POST'])
def set_night_aims(request):
    response_dic = dict()
    aims_dic = request.data.get('aim_dic')
    for aim in aims_dic:
        role = Role.objects.get(name=RoleEnum(aim))
        if aims_dic[aim] != '':
            user = User.objects.get(username=aims_dic[aim])
            player = Player.objects.get(user=user)
            decrease_limit(role, player.game)
            if role.name == str(RoleEnum.detective):
                response_dic.update({role.name: player.role.team})
            make_buff(role, player)

    return Response(response_dic)


def end_game(game):
    players = game.player_set
    citizen_count = 0
    mafia_count = 0
    independent_count = 0
    for player in players.all():
        if player.role.team == str(TeamEnum.citizen):
            if player.status:
                citizen_count += 1
        elif player.role.team == str(TeamEnum.mafia):
            if player.status:
                mafia_count += 1
        elif player.role.team == str(TeamEnum.independence):
            if player.status:
                independent_count += 1

    if mafia_count >= (citizen_count + independent_count + mafia_count) / 2:
        return str(TeamEnum.mafia)
    if mafia_count == 0 and independent_count == 0:
        return str(TeamEnum.citizen)
    else:
        return False


@api_view(['POST', 'GET'])
def voting(request):  # TODO for elnaz
    return Response()
