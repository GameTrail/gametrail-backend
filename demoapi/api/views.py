from rest_framework.viewsets import ModelViewSet
from demoapi.models import DemoApi
from demoapi.api.serializers import DemoApiSerializer

class DemoApiViewSet(ModelViewSet):
    serializer_class = DemoApiSerializer
    queryset = DemoApi.objects.all()