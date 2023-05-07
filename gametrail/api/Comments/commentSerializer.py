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
    
class CUDCommentsSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'