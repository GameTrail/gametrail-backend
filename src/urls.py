from django.contrib import admin
from django.urls import path, include
from gametrail.api.views import Logout, CustomAuthToken
from gametrail.api.views import Logout
from gametrail.api.views import CUDGameApiViewSet, GetGameApiViewSet
# Importar rutas de la API de prueba 'demoapi'
from gametrail.api.routers import router_api
from gametrail.api import views
from rest_framework.authtoken import views as token_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_api.urls)),    
    path('api/auth/logout', Logout.as_view()),
    path('api/auth/login', CustomAuthToken.as_view(), name='token_obtain_pair'),
    path('api/game', CUDGameApiViewSet.as_view()),
    path('api/populate_sabias_que', views.populate_sabias_que),
    path('api/comment', views.CUDCommentsAPIViewSet.as_view()),
    path('api/trail/', views.TrailApiViewSet.as_view()),
    path('api/gameInTrail', views.GameInTrailViewSet.as_view()),
]
