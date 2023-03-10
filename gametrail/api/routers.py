from rest_framework.routers import DefaultRouter
from gametrail.api.views import GameApiViewSet
from gametrail.api.views import UserInTrailViewSet
from gametrail.api.views import AllUserInTrailViewSet

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GameApiViewSet, basename='game')
router_api.register(prefix='trail/user', viewset=AllUserInTrailViewSet, basename='trail/user')