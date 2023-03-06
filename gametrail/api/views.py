from rest_framework.viewsets import ModelViewSet
from gametrail.models import Game
from gametrail.api.serializers import GameSerializer

class GameApiViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()