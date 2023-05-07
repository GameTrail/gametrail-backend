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
