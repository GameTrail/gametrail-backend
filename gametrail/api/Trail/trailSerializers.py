from rest_framework.serializers import ModelSerializer
from gametrail.models import *
from gametrail.api.Game.gameSerializers import *
from gametrail.api.Comments.commentSerializer import *

from rest_framework import serializers
# Django
from django.contrib.auth import password_validation, authenticate
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator, FileExtensionValidator
from django.conf import settings
# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class GetMinRatingTrailSerializer(ModelSerializer):
    class Meta:
        model = MinRatingTrail
        fields = '__all__'

class UserInTrailSerializer(ModelSerializer):
    class Meta:
        model = UserInTrail
        fields = '__all__'

class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = ['platform']

class AllUsersInTrailsSerializer(ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    avatar = serializers.CharField(source='user.avatar')
    plan = serializers.CharField(source='user.plan')

    class Meta:
        model = UserInTrail
        fields = ('id','username','email','avatar','plan')
        
class GameInTrailSerializer(ModelSerializer):
    class Meta:
        model = GameInTrail
        fields = '__all__'

class PutGameInTrailSerializer(ModelSerializer):
    game = serializers.IntegerField(source='trails.id')
    trail = serializers.IntegerField(source='games.id')
    class Meta:
        model = GameInTrail
        fields = ['id','trail','game','message' ,'priority', 'status']

class GamesInTrailsSerializer(ModelSerializer):
    games = GetGameSerializer(source='game', read_only=True)

    class Meta:
        model = GameInTrail
        fields = ('games', 'priority', 'message', 'status')

class Games1InTrailsSerializer(ModelSerializer):

    id = serializers.IntegerField(source='game.id')
    name = serializers.CharField(source='game.name')
    releaseDate = serializers.CharField(source='game.releaseDate')
    image = serializers.CharField(source='game.image')
    photos = serializers.CharField(source='game.photos')
    description = serializers.CharField(source='game.description')
    genres = serializers.SerializerMethodField()
    platform = serializers.SerializerMethodField()
    comments_games = serializers.SerializerMethodField()
    comments_games = CommentsOfAGameSerializer(many = True, read_only = True, source='game.comments_games')
    message = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    
    def get_genres(self, obj):
        return [genre.genre for genre in obj.game.genres.all()]
    def get_platform(self, obj):
        return [platform.platform for platform in obj.game.platforms.all()]

    def get_message(self, obj):

        gameintrail = GameInTrail.objects.get(pk=obj.id)
        if gameintrail:
            message =  gameintrail.message
           
            return  message
        return None
    
    def get_priority(self, obj):
        gameintrail = GameInTrail.objects.get(pk=obj.id)
        if gameintrail:
            priority =  gameintrail.priority
            return priority   
            
        return None
    
    def get_status(self, obj):
        gameintrail = GameInTrail.objects.get(pk=obj.id)
        if gameintrail:
            status =  gameintrail.status
            return  status       
               
        return None
    
   
    class Meta:
        model = Game
        fields = ('id','name','releaseDate','image','photos','description','genres','platform','comments_games','message','priority','status')
    

class OwnerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'email']

class TrailSerializer(ModelSerializer):
    games= Games1InTrailsSerializer(many=True,read_only=True)
    users=AllUsersInTrailsSerializer(many=True,read_only=True)
    platforms= serializers.SerializerMethodField()
    owner = OwnerSerializer()


    def get_platforms(self, obj):
        return [platform.platform for platform in obj.platforms.all()]
           
    class Meta:
        model = Trail
        fields = ['id', 'name', 'description', 'startDate','finishDate','maxPlayers','owner','platforms','games','users']

class UserTrailRecommendation(ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserInTrail
        fields = ['id', 'username']


class GameImageSerializer(ModelSerializer):
    image = serializers.CharField(source='game.image')
    class Meta:
        model = GameInTrail
        fields = ['image']

class RecommendedTrailSerializer(ModelSerializer):
    users = UserTrailRecommendation(many=True,read_only=True)
    games = GameImageSerializer(many=True,read_only=True)

    class Meta:
        model = Trail
        fields = ['id', 'name', 'description', 'startDate', 'finishDate', 'maxPlayers', 'users', 'games']

class PostTrailSerializer(ModelSerializer):

    class Meta:
        model = Trail
        fields = fields = ['id', 'name', 'description', 'startDate','finishDate','maxPlayers','owner']

class PutTrailSerializer(ModelSerializer):

    class Meta:
        model = Trail
        fields = ['id','name', 'description', 'startDate', 'finishDate','maxPlayers','owner']

class CTrailPatrocinedSerializer(ModelSerializer):

    class Meta:
        model = TrailPatrocinado
        fields = '__all__'

class TrailPatrocinedSerializer(ModelSerializer):

    trail = TrailSerializer(read_only = True)

    class Meta:
        model = TrailPatrocinado
        fields = ['trail']