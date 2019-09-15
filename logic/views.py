from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MGA.models import Event, User
from logic import buffLibrary
from logic.models import Role, Game, Player, Duration, RoleEnum, PlayerBuff, TeamEnum, BuffType, WakeUpEnum
from logic.serializers import RoleSerializer, GameSerializer, PlayerSerializer

"""
playerbuff va player dastiye va send_role(buff lib)
"""

killer_role_list_with_another = [RoleEnum.terrorist.value, RoleEnum.bomb_maker.value, RoleEnum.victim.value]


def get_players_except_one(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    role_name = request.data.get('role_name')
    players = game.player_set
    return_players = list()
    for player in players:
        if not player.role.name == role_name:
            return_players.append(player)

    serializer = PlayerSerializer(return_players, many=True)
    return Response(serializer.data)


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
            player = Player.objects.create(status=True, user=member, role=role_obj, game=game,
                                           limit=role_obj.limit,
                                           wake_up_limit=WakeUpEnum.get_wakeUpEnum_by_wake_up_name(
                                               role_obj.wake_up).value)
            for buff in player.role.own_buffs.all():
                if player.role.team == TeamEnum.werewolf and buff.type == BuffType.Reverse_kill.value:
                    player_buff = make_player_buff(buff, RoleEnum.hunter)
                else:
                    player_buff = make_player_buff(buff, role_obj.name)
                player.buffs.add(player_buff)

            player.save()

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
    return
    # for buff in player.buffs.all():
    #     for n_buff in buff.neutralizer.all():
    #         for buffNeu in player.buffs.all():
    #             if buffNeu.type == n_buff.type:
    #                 buffNeu.delete()
    #                 buff.delete()


def set_buff_effect(player):
    for buff in player.buffs.all():
        if buff.function_name:
            method_to_call = getattr(buffLibrary, buff.function_name)
            method_to_call(buff, player)


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
        if player.wake_up_limit == 0:
            player.wake_up_limit = WakeUpEnum.get_wakeUpEnum_by_wake_up_name(
                player.role.wake_up).value
            player.save()

            limited_role_awake(player, dictionary, RoleEnum.magician)

            role_awake(player, dictionary, RoleEnum.night_slept)

            role_awake(player, dictionary, RoleEnum.marshal)

            limited_role_awake(player, dictionary, RoleEnum.psychoanalyst)

            role_awake(player, dictionary, RoleEnum.criminal)

            role_awake(player, dictionary, RoleEnum.half_breed)

            role_awake(player, dictionary, RoleEnum.priest)

            role_awake(player, dictionary, RoleEnum.wolfman)

            role_awake(player, dictionary, RoleEnum.hero)

            role_awake(player, dictionary, RoleEnum.doctor)

            role_awake(player, dictionary, RoleEnum.detective)

            role_awake(player, dictionary, RoleEnum.simin)

            limited_role_awake(player, dictionary, RoleEnum.jailer)

            limited_role_awake(player, dictionary, RoleEnum.surgeon)

            limited_role_awake(player, dictionary, RoleEnum.dentist)

            role_awake(player, dictionary, RoleEnum.jesus)

            role_awake(player, dictionary, RoleEnum.charlatan)

            limited_role_awake(player, dictionary, RoleEnum.burial)

            limited_role_awake(player, dictionary, RoleEnum.grave_digger)

            limited_role_awake(player, dictionary, RoleEnum.snide)

        else:
            player.wake_up_limit -= 1
            player.save()

    # dictionary.update({RoleEnum.mafia: True})
    #
    # doctors = []
    # detectives = []
    #
    # for p in players:
    #     if Role.name == RoleEnum.doctor:
    #        # dictionary.update({RoleEnum.doctor: p.stauts})
    #        doctors.append(p)
    # else:
    #     if Role.name == RoleEnum.detective:
    #       #  dictionary.update({RoleEnum.detective: p.stauts})
    #        detectives.append(p)

    return Response(dictionary)


def alive_player(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    players = game.player_set

    alive_players = []
    for p in players:
        if p.stauts:
            alive_players.append(p.user.username)

    serializer = PlayerSerializer(alive_players, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


def can_put_buff(player):
    for ability in player.role.abilities.all():
        for buff in ability.buffs.all():
            if str(buff.type) == str(BuffType.NotChange_announce):
                return 1
            if str(buff.type) == str(BuffType.mirror):
                return -1
    return 0


def make_player_buff(buff, role_name):
    player_buff = PlayerBuff.objects.create(duration=buff.duration, type=buff.type,
                                            priority=buff.priority, announce=buff.announce,
                                            function_name=buff.function_name, put_player_role=role_name,
                                            player_duration=Duration.get_duration_by_duration_name(
                                                buff.duration).value)
    return player_buff


def check_neu_on_put_buff(buff, player):
    for neu in buff.neutralizer.all():
        for player_buff in player.buffs.all():
            if player_buff.type == neu.type:
                player_buff.delete()
                print()
                print(buff.type)
                print(player_buff.type)
                return False

    return True


def can_attack(player):
    for buff in player.buffs.all():
        if buff.type == str(BuffType.can_not_use_ability.value):
            return False
    return True


def make_buff(attacker, role, opponent):
    can_use_ability = can_attack(attacker)
    if not can_use_ability:
        return
    buff_result = can_put_buff(opponent)
    if buff_result != 1:
        abilities = role.abilities

        for ability in abilities.all():
            buffs = ability.buffs
            for buff in buffs.all():
                if buff_result == 0:
                    if check_neu_on_put_buff(buff, opponent):
                        player_buff = make_player_buff(buff, role.name)
                        for n in buff.neutralizer.all():
                            player_buff.neutralizer.add(n)
                        player_buff.save()
                        opponent.buffs.add(player_buff)
                        opponent.save()
                if buff_result == -1:
                    if check_neu_on_put_buff(buff, attacker):
                        player_buff = make_player_buff(buff, role.name)
                        for n in buff.neutralizer.all():
                            player_buff.neutralizer.add(n)
                        player_buff.save()
                        attacker.buffs.add(player_buff)
                        attacker.save()


def decrease_limit(role, game):
    players = game.player_set
    for player in players.all():
        if str(player.role.name) == str(role.name):
            player.limit -= 1
            player.save()
            return player
    return None


@api_view(['POST'])
def set_night_aims(request):
    response_dic = dict()
    aims_dic = request.data.get('aim_dic')
    for aim in aims_dic:
        role = Role.objects.get(name=RoleEnum(aim))
        if aims_dic[aim] != '':
            user = User.objects.get(username=aims_dic[aim])
            player = Player.objects.get(user=user)
            attacker = decrease_limit(role, player.game)
            if aim == RoleEnum.charlatan.value and player.role.name == RoleEnum.spy.value:
                make_buff(attacker, Role.objects.get(name=RoleEnum.killer.value), player)
            elif aim == RoleEnum.marshal.value:
                if player.role.name == RoleEnum.criminal.value or player.role.team == str(TeamEnum.mafia):
                    make_buff(attacker, Role.objects.get(name=RoleEnum.killer.value), player)
                elif player.role.team == str(TeamEnum.citizen):
                    make_buff(attacker, Role.objects.get(name=RoleEnum.killer.value), attacker)
            elif aim == RoleEnum.magician.value and player.role.name == RoleEnum.night_slept.value:
                make_buff(attacker, Role.objects.get(name=RoleEnum.killer.value), player)
            elif aim == RoleEnum.night_slept.value and player.role.name == RoleEnum.magician.value:
                make_buff(attacker, Role.objects.get(name=RoleEnum.killer.value), attacker)

            else:
                make_buff(attacker, role, player)

    return Response(response_dic)


@api_view(['POST', 'GET'])
def ask_god(request):
    game_id = request.data.get('game_id')
    role = request.data.get('role_name')
    player_username = request.data.get('player_username')
    game = Game.objects.get(id=game_id)
    players = game.player_set
    asked_player = None
    for player in players.all():
        if player.user.username == player_username:
            asked_player = player
            break
    if not asked_player:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if role == str(RoleEnum.detective.value):
        for buff in asked_player.buffs:
            if buff.type == str(BuffType.Reverse_inquiry_detective.value):
                return Response(TeamEnum.citizen.value, status=status.HTTP_200_OK)
        return Response(asked_player.role.team, status=status.HTTP_200_OK)

    elif role == str(RoleEnum.simin.value):
        for buff in asked_player.buffs:
            if buff.type == str(BuffType.Reverse_inquiry_simin.value):
                return Response(asked_player.role.name != str(RoleEnum.wolfman.value), status=status.HTTP_200_OK)
        return Response(asked_player.role.name == str(RoleEnum.wolfman.value), status=status.HTTP_200_OK)

    elif role == str(RoleEnum.grave_digger.value):
        if asked_player.status:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for buff in asked_player.buffs:
            if buff.type == str(BuffType.can_not_know_role.value):
                return Response('Nothing!', status=status.HTTP_200_OK)
        return Response({asked_player.user.username: asked_player.role.name}, status=status.HTTP_200_OK)


def end_game(game):
    players = game.player_set
    citizen_count = 0
    mafia_count = 0
    independent_count = 0
    werewolf_count = 0
    criminal_count = 0
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
        elif player.role.team == str(TeamEnum.werewolf):
            if player.status:
                werewolf_count += 1
        elif player.role.team == str(TeamEnum.criminals):
            if player.status:
                criminal_count += 1

    if mafia_count >= (players.all().count()) / 2:
        return str(TeamEnum.mafia)
    if mafia_count == 0 and independent_count == 0:
        return str(TeamEnum.citizen)
    if werewolf_count >= (players.all().count()) / 2:
        return str(TeamEnum.werewolf)
    if criminal_count != 0 and citizen_count == 1:
        return str(TeamEnum.criminals)
    else:
        return False


@api_view(['POST', 'GET'])
def voting(request):  # TODO for elnaz
    return Response()


@api_view(['POST', 'GET'])
def dead_with_another_person(request):
    role = request.data.get('role')
    killer = request.data.get('killer_username')
    attacked = request.data.get('attacked_username')
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    players = game.player_set

    killer_player = None
    attacked_player = None
    for player in players:
        if player.user.username == killer:
            killer_player = player
        elif player.user.username == attacked:
            attacked_player = player

    if killer_player.role.name != role:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if Role.objects.get(name=role) in killer_role_list_with_another:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    attacked_player.status = False
    killer_player.status = False


def get_dead_people(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    dead_list = list()
    for player in game.player_set.all():
        dead_list.append(player)
    serializer = PlayerSerializer(dead_list, many=True)
    return Response(serializer.data)


def get_alive_boss(request):
    game_id = request.data.get('game_id')
    game = Game.objects.get(id=game_id)
    players = game.player_set
    don = None
    mistress = None
    for player in players:
        if player.role.name == RoleEnum.don.value:
            don = player
        if player.role.name == RoleEnum.mistress.value:
            mistress = player

    if don and don.stats:
        return Response({don.role.name: don.status}, status=status.HTTP_200_OK)
    if mistress and mistress.status:
        return Response({mistress.role.name: mistress.status}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def to_die(player):  # for offline mode voting
    player.status = False


@api_view(['POST', 'GET'])
def disable_vote(request):
    user = request.user
    player = Player.objects.get(user=user)
    for buff in player.buffs:
        if buff.type == str(BuffType.Can_not_vote):
            return False
    return True


@api_view(['POST', 'GET'])
def cancel_by_mayor(request):
    user = request.user
    player = Player.objects.get(user=user)
    if player.role.name != RoleEnum.mayor.value:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        player.limit -= 1
        player.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def mayor_can_cancel(request):
    user = request.user
    player = Player.objects.get(user=user)
    if player.limit == 0:
        return False
    return True


@api_view(['POST', 'GET'])
def exit_player_by_judge(request):
    user = request.user
    player = Player.objects.get(user=user)
    if player.role.name != RoleEnum.judge.value:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        player.limit -= 1
        player.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def judge_can_exit(request):
    user = request.user
    player = Player.objects.get(user=user)
    if player.limit == 0:
        return False
    return True
