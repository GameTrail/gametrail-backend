from rest_framework.viewsets import ModelViewSet

from django.http import HttpResponse
from gametrail import functions
from gametrail.models import *
from gametrail.api.serializers import *

from django_filters.rest_framework import DjangoFilterBackend

class GameApiViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()


def populate_database_little(request):
    result = functions.populate_database(True,base_json="./src/population/develop_database_little.json")
    if result:
        html = '<html><body>Database populated successfully with low data</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate_database_big(request):
    result = functions.populate_database(True,base_json="./src/population/develop_database.json")
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
    result = functions.populate(True,base_json="./src/population/develop_database_little.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of genres, games, and platforms</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

class TrailApiViewSet(ModelViewSet):
    serializer_class = TrailSerializer
    queryset = Trail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['owner']

class RatingApiViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['ratedUser', 'userWhoRate']


class MinRatingTrailApiViewSet(ModelViewSet):
    serializer_class = MinRatingTrailSerializer
    queryset = MinRatingTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['trail']

class GameInTrailViewSet(ModelViewSet):
    serializer_class = GameInTrailSerializer
    queryset = GameInTrail.objects.all()

class GamesInTrailViewSet(ModelViewSet):

    http_method_names = ['get']
    serializer_class = GamesInTrailsSerializer
    queryset = GameInTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['trail']