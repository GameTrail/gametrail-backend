from rest_framework.viewsets import ModelViewSet
from django.http import HttpResponse
from gametrail import functions

from gametrail.models import *
from gametrail.api.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class GameApiViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class UserApiViewSet(ModelViewSet):
    http_method_names = ['get', 'delete', 'post']
    serializer_class = GetUserSerializer
    queryset = User.objects.all()

class UsersApiViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetUserSerializer
    queryset = User.objects.all()

class Logout(APIView):
    def post(self,request, format = None):
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)
    
class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk
        })

class CreateUserApiViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        """User sign up."""
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

class GameListApiViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = GameListSerializer
    queryset = GameList.objects.all()

class GameInListApiViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put']
    serializer_class = GameInListSerializer
    queryset = GameInList.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['gameList__user']

def populate_database_little(request):
    result = functions.populate_database(True,base_json="./src/population/develop_database_little.json")
    if result:
        html = '<html><body>Database populated successfully with low data</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate_database_big(request):
    result = functions.populate_database(True,base_json="./src/population/database.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of data</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate_genres(request):
    result = functions.populate_genres(True,base_json="./src/population/develop_database_genres.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of genres</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)

def populate(request):
    result = functions.populate(True,base_json="./src/population/database.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of genres, games, and platforms</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

    return HttpResponse(html)


class TrailApiViewSet(ModelViewSet):
    serializer_class = TrailSerializer
    queryset = Trail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['owner']

class RatingApiViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['ratedUser', 'userWhoRate']


class MinRatingTrailApiViewSet(ModelViewSet):
    serializer_class = MinRatingTrailSerializer
    queryset = MinRatingTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['trail']
    
class SabiasqueApiViewSet(ModelViewSet):
    serializer_class = SabiasQueSerializer
    queryset = SabiasQue.objects.all()


class GameInTrailViewSet(ModelViewSet):
    serializer_class = GameInTrailSerializer
    queryset = GameInTrail.objects.all()

class GamesInTrailViewSet(ModelViewSet):

    http_method_names = ['get']
    serializer_class = GamesInTrailsSerializer
    queryset = GameInTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['trail']

   
class UserInTrailViewSet(ModelViewSet):
    serializer_class = UserInTrailSerializer
    queryset = UserInTrail.objects.all()

class AllUserInTrailViewSet(ModelViewSet):

    http_method_names = ['get']
    serializer_class = AllUsersInTrailsSerializer
    queryset = UserInTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['trail']

class CommentsByUserId(ModelViewSet):    
    http_method_names = ['get']
    def get_queryset(self):
        commentQueryset = Comment.objects.filter(userCommented_id=self.request.headers.get("userId"))
        return commentQueryset 

    serializer_class = CommentsByUserIdSerializer

class GameCommentAPIView(ModelViewSet):
    http_method_names = ['get']
    serializer_class = CommentsOfAGameSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id', None)
        queryset = Comment.objects.filter(game_id=game_id)
        return queryset