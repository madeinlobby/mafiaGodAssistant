from rest_framework import serializers
from .models import Game

from logic.models import Role


class GameSerializer(serializers.ModelSerializer):
    class meta:
        model = Game
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
