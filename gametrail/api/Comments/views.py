from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from gametrail import functions
from django.db.models import Avg
from gametrail.models import *
from gametrail.api.serializers import *
from gametrail.api.Trail.trailSerializers import *
from gametrail.api.Trail.views import *
from gametrail.api.Game.views import *
from itertools import chain
from django.db.models.query import QuerySet
from datetime import datetime
from django.core import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

class CommentsByUserId(ModelViewSet):    
    http_method_names = ['get']
    def get_queryset(self):
        commentQueryset = Comment.objects.filter(userCommented_id=self.request.query_params.get("user_id"))
        return commentQueryset 

    serializer_class = CommentsByUserIdSerializer

class CUDCommentsAPIViewSet(APIView):
    http_method_names = ['post', 'delete']
    serializer_class = CUDCommentsSerializer
    
    def post(self, request, format=None):
        userWhoComments = User.objects.filter(id=request.data['userWhoComments'])
        is_user_valid = request.user.userName == userWhoComments[0].userName

        if is_user_valid == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif is_user_valid == True:
            serializer = CUDCommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def delete(self, request, format=None):
        if not request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                comment = Comment.objects.get(id=request.data['commentId'])
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class GameCommentAPIView(ModelViewSet):
    http_method_names = ['get']
    serializer_class = CommentsOfAGameSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id', None)
        queryset = Comment.objects.filter(game_id=game_id)
        return queryset
    
