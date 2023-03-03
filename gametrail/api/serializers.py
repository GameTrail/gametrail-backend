from rest_framework.serializers import ModelSerializer
from gametrail.models import *

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'