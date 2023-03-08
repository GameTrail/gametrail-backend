from rest_framework.viewsets import ModelViewSet
from gametrail.models import Game, Rating, MinRatingTrail
from gametrail.api.serializers import GameSerializer, RatingSerializer, MinRatingTrailSerializer
from django_filters.rest_framework import DjangoFilterBackend

class GameApiViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

class RatingApiViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['ratedUser']


class MinRatingTrailApiViewSet(ModelViewSet):
    serializer_class = MinRatingTrailSerializer
    queryset = MinRatingTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['trail']