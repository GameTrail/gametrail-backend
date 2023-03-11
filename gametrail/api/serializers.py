from rest_framework.serializers import ModelSerializer
from gametrail.models import *

class GameSerializer(ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

class MinRatingTrailSerializer(ModelSerializer):
    class Meta:
        model = MinRatingTrail
        fields = '__all__'

class TrailSerializer(ModelSerializer):
    class Meta:
        model = Trail
        fields = '__all__'

"""class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'"""