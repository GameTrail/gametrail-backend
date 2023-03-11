from rest_framework.viewsets import ModelViewSet
from gametrail.models import *
from gametrail.api.serializers import *
from django_filters.rest_framework import DjangoFilterBackend

class GameApiViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

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