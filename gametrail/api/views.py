from rest_framework.viewsets import ModelViewSet
from gametrail.models import Game
from gametrail.models import UserInTrail
from gametrail.api.serializers import GameSerializer
from gametrail.api.serializers import UserInTrailSerializer
from gametrail.api.serializers import AllUsersInTrailsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets

class GameApiViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

class UserInTrailViewSet(ModelViewSet):
    serializer_class = UserInTrailSerializer
    queryset = UserInTrail.objects.all()

class AllUserInTrailViewSet(ModelViewSet):

    http_method_names = ['get']


    serializer_class = AllUsersInTrailsSerializer
    queryset = UserInTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['trail']