from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from gametrail import functions
from django.db.models import Avg
from gametrail.models import *
from gametrail.api.Trail.trailSerializers import *
from gametrail.api.Trail.views import *
from gametrail.api.Authentication.views import check_user_is_admin
from gametrail.api.serializers import StandardResultsSetPagination
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
from itertools import chain
from django.db.models.query import QuerySet
from datetime import datetime
from django.core import serializers
from rest_framework.pagination import PageNumberPagination


class GetGameApiViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetGameSerializer
    queryset = Game.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['platforms__platform','genres__genre']
    pagination_class = StandardResultsSetPagination


class GetRecentGames(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetGameSerializer
    queryset = Game.objects.all().order_by("-id")[:10]
    
class CUDGameApiViewSet(APIView):
    http_method_names = ['post', 'put', 'delete']
    serializer_class = CUDGameSerializer

    def post(self, request, format = None):
        is_user_admin = check_user_is_admin(request)

        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = CUDGameSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format = None):
        is_user_admin = check_user_is_admin(request)

        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                game = Game.objects.get(pk=request.data['id'])
            except Game.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = CUDGameSerializer(game, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format = None):
        is_user_admin = check_user_is_admin(request)
        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                game = Game.objects.get(pk=request.data['id'])
            except Game.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            game.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        