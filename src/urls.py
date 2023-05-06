from django.contrib import admin
from django.urls import path, include
from gametrail.api.views import Logout, CustomAuthToken, CUGameInListApiViewSet
from gametrail.api.views import CUDGameApiViewSet, GetGameApiViewSet, CTrailPatrocinedViewSet, GetTrailPatrocinedViewSet
# Importar rutas de la API de prueba 'demoapi'
from gametrail.api.routers import router_api
from gametrail.api import views
from rest_framework.authtoken import views as token_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_api.urls)),    
    path('api/auth/logout', Logout.as_view()),
    path('api/gameList/game', CUGameInListApiViewSet.as_view()),
    path('api/auth/login', CustomAuthToken.as_view(), name='token_obtain_pair'),
    path('api/game', CUDGameApiViewSet.as_view()),
    path('api/populate_sabias_que', views.populate_sabias_que),
    path('api/comment', views.CUDCommentsAPIViewSet.as_view()),
    path('api/rating', views.POSTRatingAPIViewSet.as_view()),
    path('api/trail/', views.TrailApiViewSet.as_view()),
    path('api/gameInTrail', views.GameInTrailViewSet.as_view()),
    path('api/createMinRating', views.CreateMinRatingViewSet.as_view()),
    path('api/addUserInTrail', views.AddUserInTrailViewSet.as_view()),
    path('api/iaGameList',views.GameListImageIA.as_view()),
    path('api/patrocinedTrail', CTrailPatrocinedViewSet.as_view()),
    # path('api/getPatrocinedTrail', GetTrailPatrocinedViewSet.as_view())
    #path('api/trailRecomendation', views.UserTrailRecomendationViewSet.as_view())
    #path('api/tesseract_image_read', views.tesseract_image_read),
    #path('api/populate',views.populate),
]
