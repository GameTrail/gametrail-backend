from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from gametrail import functions
from django.db.models import Avg
from gametrail.models import *
from gametrail.api.serializers import *
from gametrail.api.Trail.trailSerializers import *
from gametrail.api.Authentication.authSerializer import *
from gametrail.api.Trail.views import *
from gametrail.api.Game.views import *
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

def check_user_is_admin(request):
    user = request.user
    return user.is_staff
def check_user_is_the_same(request,usergametrail):
    user = request.user
    return user.username == usergametrail.username

def check_user_is_authenticated(request):
    user = request.user
    return user.is_authenticated

class UserApiViewSet(ModelViewSet):
    http_method_names = ['get', 'delete', 'put']
    serializer_class = GetUserSerializer
    queryset = User.objects.all()
    
    def delete(self, request, format = None):
        is_user_valid = request.user.is_staff | (request.user.username == User.objects.get(pk=request.data['userId']).username)
        if is_user_valid == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = User.objects.get(pk=request.data['userId'])
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            user.delete()
            user_django = user_django.objects.get(username=user.username)
            user_django.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, format = None):
        user = request.user
        if not (request.user.username == User.objects.get(pk=request.data.get("userId")).username):            
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        else:            
            try:
                user = User.objects.get(pk=request.data.get("userId"))
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = PutUserSerializer(user, data=request.data)
            if serializer.is_valid():
                if (request.data.get("password") != None):
                    user_django = user_django.objects.get(username=request.user.username)
                    user_django.set_password(request.data.get("password"))

                    serializer.save()

                    user = User.objects.get(pk=request.data.get("userId"))
                    user.set_password(request.data.get("password"))
                    user.save()   
                             
                    user_django.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:                
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    def post(self,request, format = None):
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)
    
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        user.username
        return Response({
            'token': token.key,
            'user_id': User.objects.get(username=user.username).id
        })

class CreateUserApiViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        """User sign up."""
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)
    
class GameListApiViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = GameListSerializer
    queryset = GameList.objects.all()

class GameInListApiViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GameInListSerializer
    queryset = GameInList.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['gameList__user']

class CUGameInListApiViewSet(APIView):
    http_method_names = ['post', 'put']
    serializer_class = CUGameInListSerializer

    def post(self, request, format=None):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            userName = request.user.username
            ownerList = User.objects.get(pk = request.data['user'])
        
            if userName != ownerList.username:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                gameList = GameList.objects.get(user_id = request.data['user'])
                request.data['gameList'] = gameList.id
                serializer = CUGameInListSerializer(data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, format=None):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            userName = request.user.username
            ownerList = User.objects.get(pk = request.data['user'])
        
            if userName != ownerList.username:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                gameList = GameList.objects.get(user_id = request.data['user'])
                gameInList = GameInList.objects.filter(gameList_id = gameList.id, game_id = request.data['game'])[0]
                print(gameInList)
                if gameInList.gameList.id != gameList.id:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                
                request.data.pop("user")
                request.data["gameList"] = gameList.id

                serializer = CUGameInListSerializer(gameInList, data = request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)

class RatingApiViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['ratedUser', 'userWhoRate']

        
class POSTRatingAPIViewSet(APIView):

    http_method_names = ['post']
    serializer_class = RatingSerializer
    
    def post(self, request, format=None): 

        userWhoRate= User.objects.filter(id=request.data['userWhoRate'])
        is_user_valid = request.user.username == userWhoRate[0].username

        rating_data = request.data.get("rating", None)
        if is_user_valid:    
            if rating_data is not None and len(rating_data) <= 5:# and is_user_valid:
                
                ratings = []

                for rating_type, rating_value in rating_data.items(): 
                    rating = {
                        "ratedUser": request.data.get("ratedUser"),
                        "userWhoRate": request.data.get("userWhoRate"),
                        "rating": rating_value,
                        "type": rating_type
                    } 
                    serializer = RatingSerializer(data=rating)
                    
                    if serializer.is_valid():
                        serializer.save()
                        ratings.append(serializer.data)

                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                return Response(ratings, status=status.HTTP_201_CREATED)
            
            else:
                return Response({"error": "You must include between 1 and 5 ratings"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class UpdateSubscriptionAPIViewSet(ModelViewSet):
    http_method_names = ['put']
    serializer_class = UserSerializersub
    @classmethod
    
    def put(self, request, format=None):
        user_id = request.data['userId']
        action = request.data['action']
        usergametrail = User.objects.get(id=user_id)
        is_user_same = check_user_is_the_same(request,usergametrail)

        if is_user_same == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = User.objects.get(id=user_id)
                if action == 'SUBSCRIBE':
                    user.plan = 'Premium'
                    user.suscription_time =  datetime.now().date()
                elif action == 'UNSUBSCRIBE':
                    user.plan = 'STANDARD'
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                user.save()
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            
            serializer = UserSerializersub(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
