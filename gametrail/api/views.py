from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from gametrail import functions
from django.db.models import Avg
from gametrail.models import *
from gametrail.api.serializers import *
from gametrail.api.Trail.trailSerializers import *
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
from rest_framework.decorators import api_view

def populate_database_little(request):
    result = functions.populate_database(True,base_json="./src/population/develop_database_little.json")
    if result:
        html = '<html><body>Database populated successfully with low data</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate_database_big(request):
    result = functions.populate_database(True,base_json="./src/population/database.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of data</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate_genres(request):
    result = functions.populate_genres(True,base_json="./src/population/develop_database_genres.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of genres</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate(request):
    result = functions.populate(True,base_json="./src/population/database.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of genres, games, and platforms</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate_sabias_que(request):
    result = functions.populate_sabias_que()
    if result:
        html = '<html><body>Database populated successfully with "Sabias que"</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>'

    return HttpResponse(html)

def populate_users(request):
    result = functions.populate_users(base_json="./src/population/users/users.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of users</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

def populate_gameLists(request):
    result = functions.populate_gameLists(base_json="./src/population/gameList/gameList.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of GameLists</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 
    return HttpResponse(html)

def populate_trails(request):
    result = functions.populate_trails(base_json="./src/population/trails/trail_copy.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of Trails</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 
    return HttpResponse(html)

def populate_comments(request):
    result = functions.populate_comments(base_json="./src/population/comments/comment.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of Comments</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 
    return HttpResponse(html)

def populate_ratings(request):
    result = functions.populate_ratings(base_json="./src/population/ratings/rating.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of Ratings</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 
    return HttpResponse(html)
   
class SabiasqueApiViewSet(ModelViewSet):
    serializer_class = SabiasQueSerializer
    queryset = SabiasQue.objects.all()

@api_view(['GET'])
def tesseract_image_read(request):
    image = request.GET.get("image")    
    html = '<html><body>Work in progress</body></html>'
    functions.tesseract_image_read(image)
    return HttpResponse(html)
class GameListImageIA(APIView):
    http_method_names = ['post']
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
                try:
                    image = request.data['image']
                    list_games_to_add = functions.tesseract_image_read(image)
                    dgameList = GameList.objects.get(user_id = request.data['user'])
                    try:
                        for dgame in list_games_to_add:
                            if dgame != None:
                                #print(dgame.id)
                                newGame = GameInList.objects.create(
                                    game = dgame, gameList = dgameList, status = "PENDING"
                                )
                                newGame.save()
                        return Response(str(len(list_games_to_add)) + " games added to list. " + str(list_games_to_add), status = status.HTTP_201_CREATED)
                    except:
                        return Response("Some games were already in list",status=status.HTTP_200_OK)

                except:            
                    return Response("Image was not read properly", status=status.HTTP_400_BAD_REQUEST)

class GetTrailPatrocinedViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = TrailPatrocinedSerializer
    queryset = TrailPatrocinado.objects.all()

class CTrailPatrocinedViewSet(APIView):
    http_method_names = ['post', 'put']
    serializer_class = CTrailPatrocinedSerializer

    def post(self, request, format = None):
        is_user_admin = check_user_is_admin(request)

        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            trailsPatrocinados = TrailPatrocinado.objects.all()
            if len(trailsPatrocinados) == 1:
                return Response("Ya existe un Trail Patrocinado creado. Modificalo con un método PUT", status=status.HTTP_400_BAD_REQUEST)

            serializer = CTrailPatrocinedSerializer(data=request.data)

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
                trail = TrailPatrocinado.objects.get(pk=1)
            except TrailPatrocinado.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CTrailPatrocinedSerializer(trail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   