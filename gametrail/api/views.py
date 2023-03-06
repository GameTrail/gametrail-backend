from rest_framework.viewsets import ModelViewSet
from gametrail.models import Game
from gametrail.api.serializers import GameSerializer
from rest_framework import filters

class GameApiViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']