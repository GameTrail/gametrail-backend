from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from gametrail.models import *
from gametrail.api.serializers import *
from django_filters.rest_framework import DjangoFilterBackend

class GameApiViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class UserApiViewSet(ModelViewSet):
    http_method_names = ['get', 'delete']
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CreateUserApiViewSet(ModelViewSet):
    http_method_names = ['post', 'put']
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()

class GameListApiViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = GameListSerializer
    queryset = GameList.objects.all()

class GameInListApiViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    serializer_class = GameInListSerializer
    queryset = GameInList.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['gameList__user']