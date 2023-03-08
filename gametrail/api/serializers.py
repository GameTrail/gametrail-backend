from rest_framework.serializers import ModelSerializer
from gametrail.models import Game
from gametrail.models import SabiasQue

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class SabiasQueSerializer(ModelSerializer):
    class Meta:
        model = SabiasQue
        fields = '__all__'