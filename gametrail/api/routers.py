from rest_framework.routers import DefaultRouter
from gametrail.api.views import GameApiViewSet
from gametrail.api.views import SabiasqueApiViewSet

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GameApiViewSet, basename='game')
router_api.register(prefix='sabiasque', viewset=SabiasqueApiViewSet, basename='sabiasque')