from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from gametrail.models import *
from gametrail.api.serializers import *

class GameApiViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class UserApiViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()