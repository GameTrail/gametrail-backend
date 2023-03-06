from rest_framework.routers import DefaultRouter
from gametrail.api.views import GameApiViewSet

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GameApiViewSet, basename='game')