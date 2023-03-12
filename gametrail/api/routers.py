from rest_framework.routers import DefaultRouter
from gametrail.api.views import *

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GameApiViewSet, basename='game')
router_api.register(prefix='user', viewset=UserApiViewSet, basename='user')
router_api.register(prefix='createUser', viewset=CreateUserApiViewSet, basename='createUser')
router_api.register(prefix='createList', viewset=GameListApiViewSet, basename='createList')
router_api.register(prefix='gameList', viewset=GameInListApiViewSet, basename='gameList')


