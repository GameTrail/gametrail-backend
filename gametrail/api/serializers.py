from rest_framework.serializers import ModelSerializer
from gametrail.models import *

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'plan']

class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class GameListSerializer(ModelSerializer):
    class Meta:
        model = GameList
        fields = '__all__'

class GameInListSerializer(ModelSerializer):
    class Meta:
        model = GameInList
        fields = '__all__'