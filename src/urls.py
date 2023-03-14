from django.contrib import admin
from django.urls import path, include

# Importar rutas de la API de prueba 'demoapi'
from gametrail.api.routers import router_api
from gametrail.api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_api.urls)),    
    path('api/populate/', views.populate),
]
