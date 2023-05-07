from rest_framework.serializers import ModelSerializer
from gametrail.models import *
from rest_framework import serializers
from gametrail.api.Comments.commentSerializer import *
# Django
from django.contrib.auth import password_validation, authenticate
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator, FileExtensionValidator
from django.conf import settings
# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class CUDGameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre']

class PlatformSerializer(ModelSerializer):
    class Meta:
        model = Platform
        fields = ['platform']


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

class GenreSerializer1(ModelSerializer):
   
    class Meta:
        model = Genre
        fields = ('genre',)
       

