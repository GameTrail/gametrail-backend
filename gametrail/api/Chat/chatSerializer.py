from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from gametrail.models import *

class ChatByTrailIdSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    trailId = serializers.SerializerMethodField()

    def get_user(self,obj):
        return {
            'id': obj.user.id,
            'username' : obj.user.username,
            'avatar': obj.user.avatar,
        }
    
    def get_trailId(self,obj):
        return obj.trail.id
        
    
    class Meta:
        model = ChatTrail
        fields = ['id', 'text', 'creationDate', 'user', 'trailId']

class PostChatSerializer(ModelSerializer):
    class Meta:
        model = ChatTrail
        fields = '__all__'