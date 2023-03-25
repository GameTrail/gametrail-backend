from rest_framework.serializers import ModelSerializer
from gametrail.models import *
from rest_framework import serializers
# Django
from django.contrib.auth import password_validation, authenticate
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator, FileExtensionValidator
from django.conf import settings
# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre']

class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = ['platform']

class GetGameSerializer(ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    platforms = PlatformSerializer(many=True, read_only=True)
    
    class Meta:
        model = Game
        fields = ['id', 'name', 'releaseDate', 'image', 'photos', 'description', 'genres', 'platforms']

class CUDGameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class SabiasQueSerializer(ModelSerializer):
    class Meta:
        model = SabiasQue
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class UserSerializersub(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'plan']

class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):

        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        self.context['user'] = user
        return data

    def create(self, data):
        """Generar o recuperar token."""
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key

class CreateUserSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    avatar = serializers.CharField()

    password = serializers.CharField()
    password_confirmation = serializers.CharField()

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Las contraseñas no coinciden")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        print(user)
        return user
    
class GameListSerializer(ModelSerializer):
    class Meta:
        model = GameList
        fields = '__all__'

class GameInListSerializer(ModelSerializer):

    game=GetGameSerializer(read_only=True)

    class Meta:
        model = GameInList
        fields = '__all__'

class CUGameInListSerializer(ModelSerializer):

    class Meta:
        model = GameInList
        fields = ['game','status','gameList']

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class GetMinRatingTrailSerializer(ModelSerializer):
    class Meta:
        model = MinRatingTrail
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
        
class GameInTrailSerializer(ModelSerializer):
    class Meta:
        model = GameInTrail
        fields = '__all__'

class GamesInTrailsSerializer(ModelSerializer):
    games = GetGameSerializer(source='game', read_only=True)

    class Meta:
        model = GameInTrail
        fields = ('games',)

class OwnerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'email']

class TrailSerializer(ModelSerializer):
    games= GamesInTrailsSerializer(many=True,read_only=True)
    users=AllUsersInTrailsSerializer(many=True,read_only=True)
    platforms=PlatformSerializer(many=True,read_only=True)
    owner = OwnerSerializer()
           
    class Meta:
        model = Trail
        fields = ['id', 'name', 'description', 'startDate','finishDate','maxPlayers','owner','platforms','games','users']

class PostTrailSerializer(ModelSerializer):

    class Meta:
        model = Trail
        fields = '__all__'

class CommentsByUserIdSerializer(ModelSerializer):
    userWhoComments = serializers.SerializerMethodField()
    commentedUser = serializers.SerializerMethodField()

    def get_userWhoComments(self,obj):
        return {
            'id': obj.userWhoComments.id,
            'username' : obj.userWhoComments.username,
            'avatar': obj.userWhoComments.avatar,
        }
    
    def get_commentedUser(self,obj):
        return {
            'id': obj.userCommented.id,
            'username': obj.userCommented.username,
            'avatar': obj.userCommented.avatar,
        }
    class Meta:
        model = Comment
        fields = ['id','commentText','commentedUser','userWhoComments']

class CommentsOfAGameSerializer(ModelSerializer):
    
    userWhoComments = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id','commentText','game','userWhoComments')

    def get_userWhoComments(self, obj):
        return {
            'id': obj.userWhoComments.id,
            'username': obj.userWhoComments.username,
            'avatar': obj.userWhoComments.avatar,
        }

class TrailFromUser(ModelSerializer):
    id = serializers.IntegerField(source='trail.id')
    name = serializers.CharField(source='trail.name')
    description = serializers.CharField(source='trail.description')
    startDate = serializers.CharField(source='trail.startDate')
    finishDate = serializers.CharField(source='trail.finishDate')
    maxPlayers = serializers.CharField(source='trail.maxPlayers')
    owner = OwnerSerializer(source='trail.owner')
    games= GamesInTrailsSerializer(many=True,read_only=True, source="trail.games")
    users=AllUsersInTrailsSerializer(many=True,read_only=True, source="trail.users")
    platforms=PlatformSerializer(many=True,read_only=True, source="trail.platforms")
    class Meta:
        model = UserInTrail
        fields = ('id','name','description','startDate','finishDate','maxPlayers', 'owner', 'games', 'users', 'platforms')
  
class GetUserSerializer(ModelSerializer):
    games=GameInListSerializer(many=True,read_only=True, source="gameList.games_in_list")
    trails=TrailFromUser(many=True,read_only=True,source="trails_with_user")
    rate_recieved=RatingSerializer(many=True, read_only=True)
    comments_received=CommentsByUserIdSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'plan', 'games', 'trails', 'rate_recieved', 'comments_received']

class PutUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar']
        
class CUDCommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'