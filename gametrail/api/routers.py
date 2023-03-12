from rest_framework.routers import DefaultRouter
from gametrail.api.views import *

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GameApiViewSet, basename='game')
router_api.register(prefix='trail', viewset=TrailApiViewSet, basename='trail')
router_api.register(prefix='rating', viewset=RatingApiViewSet, basename='rating')
router_api.register(prefix='minRating', viewset=MinRatingTrailApiViewSet, basename='minRating')
router_api.register(prefix='gamesInTrail', viewset=GamesInTrailViewSet, basename='gamesInTrail')
router_api.register(prefix='gameInTrail', viewset=GameInTrailViewSet, basename='gameInTrail')