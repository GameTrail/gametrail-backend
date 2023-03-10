from rest_framework.serializers import ModelSerializer
from gametrail.models import Game
from gametrail.models import UserInTrail
from rest_framework import serializers

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class UserInTrailSerializer(ModelSerializer):
    class Meta:
        model = UserInTrail
        fields = '__all__'

class AllUsersInTrailsSerializer(ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    avatar = serializers.CharField(source='user.avatar')
    plan = serializers.CharField(source='user.plan')

    class Meta:
        model = UserInTrail
        fields = ('id','username','email','avatar','plan')
