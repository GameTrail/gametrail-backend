from rest_framework.routers import DefaultRouter
from demoapi.api.views import DemoApiViewSet

router_demoapi = DefaultRouter()

router_demoapi.register(prefix='demoapi', viewset=DemoApiViewSet, basename='demoapi')