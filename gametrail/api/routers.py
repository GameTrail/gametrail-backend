from rest_framework.routers import DefaultRouter
from gametrail.api.views import *

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GameApiViewSet, basename='game')
router_api.register(prefix='user', viewset=UserApiViewSet, basename='user')
