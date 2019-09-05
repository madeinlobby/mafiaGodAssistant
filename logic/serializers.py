from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):

    class meta:
        model = Game
        fields = '__all__'

