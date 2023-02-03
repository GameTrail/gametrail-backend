from rest_framework.serializers import ModelSerializer
from demoapi.models import DemoApi

class DemoApiSerializer(ModelSerializer):
    class Meta:
        model = DemoApi
        fields = '__all__'