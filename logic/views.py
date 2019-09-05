from rest_framework.decorators import api_view
from rest_framework.response import Response

from MGA.models import Event
from logic.models import Role, Game
from logic.serializers import RoleSerializer, GameSerializer


@api_view(['GET'])
def get_all_roles(request):
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)


def random_roles(role_dict, game_id):
    game = Game.objects.get(game_id)
    members = game.event.members
    all = 0
    for role in role_dict:
        all += role_dict[role]

    # if all == len(members):


@api_view(['POST', 'GET'])
def set_game_role(request):
    game_id = request.data.get('game_id')
    role_dict = request.data.get('role_dict')
    random_roles(role_dict, game_id)


@api_view(['GET', 'POST'])
def create_game(request):
    event_id = request.data.get('event id')
    event = Event.objects.get(id=event_id)
    game = Game.objects.all().get()
    Game.objects.create(owner=event.owner, event=event)

    serializer = GameSerializer(game)
    return Response(serializer.data)
