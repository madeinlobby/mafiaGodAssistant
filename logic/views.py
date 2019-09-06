from random import random, randrange

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from MGA.models import Event
from logic.models import Role, Game, Player
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
        for member in members:
            for role in role_dict:
                role_value = role_dict[role]
                if role_value != 0:
                    role_dict[role] -= 1
                    role = Role.objects.get(id=role)
                    player = Player.objects.create(status=True, user=member, role=role, game=game)
                    player.save()
        game.save()
        serializer = PlayerSerializer(game.player_set, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
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
