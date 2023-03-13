from rest_framework.serializers import ModelSerializer
from gametrail.models import *
from rest_framework import serializers


class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'




class SabiasQueSerializer(ModelSerializer):
    class Meta:
        model = SabiasQue
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
        

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class MinRatingTrailSerializer(ModelSerializer):
    class Meta:
        model = MinRatingTrail
        fields = '__all__'

class TrailSerializer(ModelSerializer):
    class Meta:
        model = Trail
        fields = '__all__'

class GameInTrailSerializer(ModelSerializer):
    class Meta:
        model = GameInTrail
        fields = '__all__'

class GamesInTrailsSerializer(ModelSerializer):
    id = serializers.IntegerField(source='game.id')
    TrailName=serializers.CharField(source='trail.name')
    GameName = serializers.CharField(source='game.name')

    class Meta:
        model = GameInTrail
        fields = ('id','TrailName','GameName')