from django.shortcuts import render
from logic.models import Game
from rest_framework.response import Response
from rest_framework.decorators import api_view
from MGA.models import Event
from logic.serializers import GameSerializer



@api_view(['GET','POST'])
def create_game(request):
    event_id = request.data.get('event id')
    event = Event.objects.get(id=event_id)
    game = Game.objects.all().get()
    Game.objects.create(owner=event.owner,event=event)

    serializer = GameSerializer(game)
    return Response(serializer.data)



