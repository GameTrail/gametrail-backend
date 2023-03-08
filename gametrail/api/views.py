from rest_framework.viewsets import ModelViewSet
from gametrail.models import Game
from gametrail.api.serializers import GameSerializer
from django.http import HttpResponse
from gametrail import functions

class GameApiViewSet(ModelViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all()

def populate_database_little(request):
    result = functions.populate_database(True,base_json="./develop_database_little.json")
    if result:
        html = '<html><body>Database populated successfuly with low data</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate_database_big(request):
    result = functions.populate_database(True,base_json="./develop_database.json")
    if result:
        html = '<html><body>Database populated successfuly with a lot of data</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)