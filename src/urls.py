from django.contrib import admin
from django.urls import path, include
from gametrail.api.Trail.views import *
from gametrail.api.Game.views import *
from gametrail.api.Authentication.views import *
from gametrail.api.Chat.views import PostChatAPIViewSet

# Importar rutas de la API de prueba 'demoapi'
from gametrail.api.routers import router_api
from gametrail.api import views

from rest_framework.authtoken import views as token_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_api.urls)),    
    path('api/auth/logout', Logout.as_view()),
    path('api/edit-user', ModifyUserViewSet.as_view()),
    path('api/delete-user', DeleteUserViewSet.as_view()),
    path('api/gameList/game', CUGameInListApiViewSet.as_view()),
    path('api/auth/login', CustomAuthToken.as_view(), name='token_obtain_pair'),
    path('api/game', CUDGameApiViewSet.as_view()),
    path('api/populate_sabias_que', views.populate_sabias_que),
    path('api/comment', CUDCommentsAPIViewSet.as_view()),
    path('api/rating', POSTRatingAPIViewSet.as_view()),
    path('api/trail/', TrailApiViewSet.as_view()),
    path('api/gameInTrail', GameInTrailViewSet.as_view()),
    path('api/createMinRating', CreateMinRatingViewSet.as_view()),
    path('api/addUserInTrail', AddUserInTrailViewSet.as_view()),
    path('api/iaGameList', GameListImageIA.as_view()),
    path('api/patrocinedTrail', CTrailPatrocinedViewSet.as_view()),
    path('api/chat', PostChatAPIViewSet.as_view()),
    # path('api/getPatrocinedTrail', GetTrailPatrocinedViewSet.as_view())
    # path('api/trailRecomendation', UserTrailRecomendationViewSet.as_view())
]
