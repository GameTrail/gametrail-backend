from django.contrib import admin
from django.urls import path, include

# Importar rutas de la API de prueba 'demoapi'
from gametrail.api.routers import router_api
from gametrail.api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_api.urls)),
    path('api/populate_little/', views.populate_database_little),
    path('api/populate_big/', views.populate_database_big),
    path('api/populate_genres', views.populate_genres),
]
