from rest_framework.serializers import ModelSerializer
from gametrail.models import *
from rest_framework import serializers

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
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
    name = serializers.CharField(source='game.name')

    class Meta:
        model = GameInTrail
        fields = ('id','name')