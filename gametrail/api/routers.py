from rest_framework.routers import DefaultRouter
from gametrail.api.views import *

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GameApiViewSet, basename='game')
router_api.register(prefix='user', viewset=UserApiViewSet, basename='user')
router_api.register(prefix='createUser', viewset=CreateUserApiViewSet, basename='createUser')
router_api.register(prefix='createList', viewset=GameListApiViewSet, basename='createList')
router_api.register(prefix='gameList', viewset=GameInListApiViewSet, basename='gameList')
router_api.register(prefix='trail', viewset=TrailApiViewSet, basename='trail')
router_api.register(prefix='rating', viewset=RatingApiViewSet, basename='rating')
router_api.register(prefix='minRating', viewset=MinRatingTrailApiViewSet, basename='minRating')
router_api.register(prefix='allGamesInTrail', viewset=GamesInTrailViewSet, basename='allGamesInTrail')
router_api.register(prefix='gameInTrail', viewset=GameInTrailViewSet, basename='gameInTrail')
router_api.register(prefix='trail/allUsers', viewset=AllUserInTrailViewSet, basename='trail/allUsers')
router_api.register(prefix='trail/user', viewset=UserInTrailViewSet, basename='trail/user')