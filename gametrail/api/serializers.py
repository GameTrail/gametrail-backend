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

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class SabiasQueSerializer(ModelSerializer):
    class Meta:
        model = SabiasQue
        fields = '__all__'

class GetUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'plan']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

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