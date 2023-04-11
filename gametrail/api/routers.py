from rest_framework.routers import DefaultRouter
from gametrail.api.views import *

router_api = DefaultRouter()
router_api.register(prefix='game', viewset=GetGameApiViewSet, basename='game')
router_api.register(prefix='recentGames', viewset=GetRecentGames, basename='recentGames')
router_api.register(prefix='user', viewset=UserApiViewSet, basename='user')
router_api.register(prefix='auth', viewset=CreateUserApiViewSet, basename='auth')
router_api.register(prefix='createList', viewset=GameListApiViewSet, basename='createList')
router_api.register(prefix='gameList', viewset=GameInListApiViewSet, basename='gameList')
router_api.register(prefix='getTrail', viewset=GetTrailApiViewSet, basename='getTrail')
router_api.register(prefix='minRating', viewset=GetMinRatingTrailApiViewSet, basename='minRating')
router_api.register(prefix='sabiasque', viewset=SabiasqueApiViewSet, basename='sabiasque')
router_api.register(prefix='allGamesInTrail', viewset=GamesInTrailViewSet, basename='allGamesInTrail')
router_api.register(prefix='allUsersInTrail', viewset=AllUserInTrailViewSet, basename='allUsersInTrail')
router_api.register(prefix='userInTrail', viewset=GetUserInTrailViewSet, basename='userInTrail')
router_api.register(prefix='comment/user', viewset=CommentsByUserId, basename='commentsByUserId')
router_api.register(prefix='comment/game', viewset=GameCommentAPIView, basename='gameComments')
router_api.register(prefix='sub', viewset=UpdateSubscriptionAPIViewSet, basename='subscription')