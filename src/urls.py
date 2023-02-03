from django.contrib import admin
from django.urls import path, include

# Importar rutas de la API de prueba 'demoapi'
from demoapi.api.router import router_demoapi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demoapi/', include(router_demoapi.urls)),
]
