
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

class GameListSerializer(ModelSerializer):
    class Meta:
        model = GameList
        fields = '__all__'

class GetGameSerializer(ModelSerializer):
    genres = serializers.SerializerMethodField()
    platforms = serializers.SerializerMethodField()
    comments_games = CommentsOfAGameSerializer(many = True, read_only = True)

    def get_genres(self, obj):
        return [genre.genre for genre in obj.genres.all()]
    def get_platforms(self, obj):
        return [platform.platform for platform in obj.platforms.all()]
    
    class Meta:
        model = Game
        fields = ['id', 'name', 'releaseDate', 'image', 'photos', 'description', 'genres', 'platforms', 'comments_games']

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

class GenreSerializer1(ModelSerializer):
   
    class Meta:
        model = Genre
        fields = ('genre',)


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

class PostTrailSerializer(ModelSerializer):

    class Meta:
        model = Trail
        fields = fields = ['id', 'name', 'description', 'startDate','finishDate','maxPlayers','owner']

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
    comments_received=CommentsByUserIdSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'plan', 'games', 'trails', 'average_ratings', 'comments_received']

class PutUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar','email']
        
class CUDCommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PutTrailSerializer(ModelSerializer):

    class Meta:
        model = Trail
        fields = ['id','name', 'description', 'startDate', 'finishDate','maxPlayers','owner']