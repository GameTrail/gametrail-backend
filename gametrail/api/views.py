from rest_framework.viewsets import ModelViewSet
from gametrail.models import Game
from gametrail.models import SabiasQue
from gametrail.api.serializers import GameSerializer
from gametrail.api.serializers import SabiasQueSerializer

class GameApiViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()


class SabiasqueApiViewSet(ModelViewSet):
    serializer_class = SabiasQueSerializer
    queryset = SabiasQue.objects.all()