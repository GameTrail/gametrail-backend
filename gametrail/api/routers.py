from rest_framework.routers import DefaultRouter
from gametrail.api.views import GameApiViewSet, RatingApiViewSet, MinRatingTrailApiViewSet

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GameApiViewSet, basename='game')
router_api.register(prefix='rating', viewset=RatingApiViewSet, basename='rating')
router_api.register(prefix='minRating', viewset=MinRatingTrailApiViewSet, basename='minRating')