from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from gametrail import functions
from django.db.models import Avg
from gametrail.models import *
from gametrail.api.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from itertools import chain
from django.db.models.query import QuerySet

def check_user_is_admin(request):
    user = request.user
    return user.is_staff

def check_user_is_the_same(request,usergametrail):
    user = request.user
    return user.username == usergametrail.username

class GetGameApiViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetGameSerializer
    queryset = Game.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['platforms__platform','genres__genre']

    
class CUDGameApiViewSet(APIView):
    http_method_names = ['post', 'put', 'delete']
    serializer_class = CUDGameSerializer

    def post(self, request, format = None):
        is_user_admin = check_user_is_admin(request)

        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = CUDGameSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format = None):
        is_user_admin = check_user_is_admin(request)

        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                game = Game.objects.get(pk=request.data['id'])
            except Game.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = CUDGameSerializer(game, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format = None):
        is_user_admin = check_user_is_admin(request)
        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                game = Game.objects.get(pk=request.data['id'])
            except Game.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            game.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class UserApiViewSet(ModelViewSet):
    http_method_names = ['get', 'delete', 'put']
    serializer_class = GetUserSerializer
    queryset = User.objects.all()
    
    def delete(self, request, format = None):
        is_user_admin = request.user.is_staff
        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = User.objects.get(pk=request.data['userId'])
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, format = None):
        user = request.user
        if not (request.user.username == User.objects.get(pk=request.data.get("userId")).username):            
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        else:            
            try:
                user = User.objects.get(pk=request.data.get("userId"))
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = PutUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        user.username
        return Response({
            'token': token.key,
            'user_id': User.objects.get(username=user.username).id
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

def populate_sabias_que(request):
    result = functions.populate_sabias_que()
    if result:
        html = '<html><body>Database populated successfully with "Sabias que"</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>'

    return HttpResponse(html)


def check_user_is_authenticated(request):
    user = request.user
    return user.is_authenticated

class TrailApiViewSet(APIView):
    
    http_method_names = ['post', 'delete']
    serializer_class = TrailSerializer

    def post(self, request, format = None):
        
        if not check_user_is_authenticated(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            owner= User.objects.get(pk=request.data['owner']).username
            user = request.user.username
            
            if user != owner:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        
            serializer = PostTrailSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    trail=serializer.save()
                    trail.full_clean()
                    trail.save()
                    userInTrail = UserInTrail(user = owner, trail = trail)
                    userInTrail.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format = None):
        is_user_admin = check_user_is_admin(request)
        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                trail = Trail.objects.get(pk=request.data['id'])
            except Trail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            trail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GetTrailApiViewSet(ModelViewSet):
    
    http_method_names = ['get']
    serializer_class = TrailSerializer
    queryset = Trail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['games__game','users__user']

    
class RatingApiViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    queryset = Rating.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['ratedUser', 'userWhoRate']

class GetMinRatingTrailApiViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetMinRatingTrailSerializer
    queryset = MinRatingTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['trail']
    
class SabiasqueApiViewSet(ModelViewSet):
    serializer_class = SabiasQueSerializer
    queryset = SabiasQue.objects.all()


class GameInTrailViewSet(APIView):
    http_method_names = ['post', 'put']
    serializer_class = GameInTrailSerializer
    
    def post(self, request, format=None):
        owner= Trail.objects.get(pk=request.data['trail']).owner.username
        user = request.user.username
        
        if user != owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else :
            serializer = GameInTrailSerializer(data=request.data)
            if serializer.is_valid():
                try:
                 gameintrail=serializer.save()
                 gameintrail.full_clean()
                 gameintrail.save()
                 return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                 return Response(str(e), status=status.HTTP_400_BAD_REQUEST)          
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, format = None):
        owner= Trail.objects.get(pk=request.data['trail']).owner.username
        user = request.user.username

        if user != owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                trail = GameInTrail.objects.get(pk=request.data['id'])
            except GameInTrail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            serializer = GameInTrailSerializer(trail, data=request.data)
            if serializer.is_valid():
                try:
                 gameintrail=serializer.save()
                 gameintrail.full_clean()
                 gameintrail.save()
                 return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                 return Response(str(e), status=status.HTTP_400_BAD_REQUEST)  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            


class GamesInTrailViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GamesInTrailsSerializer
    queryset = GameInTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['trail']
   
class GetUserInTrailViewSet(ModelViewSet):
    http_method_names = ['get']
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
        commentQueryset = Comment.objects.filter(userCommented_id=self.request.query_params.get("user_id"))
        return commentQueryset 

    serializer_class = CommentsByUserIdSerializer

class GameCommentAPIView(ModelViewSet):
    http_method_names = ['get']
    serializer_class = CommentsOfAGameSerializer

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id', None)
        queryset = Comment.objects.filter(game_id=game_id)
        return queryset
        
class CUDCommentsAPIViewSet(APIView):
    http_method_names = ['post', 'delete']
    serializer_class = CUDCommentsSerializer
    
    def post(self, request, format=None):
        userWhoComments = User.objects.filter(id=request.data['userWhoComments'])
        is_user_valid = request.user.username == userWhoComments[0].username

        if is_user_valid == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif is_user_valid == True:
            serializer = CUDCommentsSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def delete(self, request, format=None):
        if not request.user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                comment = Comment.objects.get(id=request.data['commentId'])
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
class CreateMinRatingViewSet(APIView):
    http_method_names = ['post']
    serializer_class = GetMinRatingTrailSerializer

    @classmethod
    def post(self, request, format = None):
        userGameTrail = User.objects.get(pk = request.data['user'])
        is_username_same = check_user_is_the_same(request, userGameTrail)

        if is_username_same == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            owner = Trail.objects.get(pk = request.data['trail']).owner
            is_premium = owner.plan == "Premium"
            if userGameTrail != owner or not is_premium:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer = GetMinRatingTrailSerializer(data=request.data)
                if serializer.is_valid():
                    try:
                        minRating = serializer.save()
                        minRating.full_clean()
                        minRating.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)     
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def check_min_ratings(user, trail):
    min_ratings = MinRatingTrail.objects.filter(trail = trail)
    for min_rating in min_ratings:
        min = min_rating.minRating
        type = min_rating.ratingType
        ratings_user = Rating.objects.filter(ratedUser_id = user, type = type).aggregate(Avg('rating'))['rating__avg']
        if ratings_user == None or ratings_user < min:
            return False
    return True

class AddUserInTrailViewSet(APIView):
    http_method_names = ['post']
    serializer_class = UserInTrailSerializer

    @classmethod
    def post(self, request, format = None):
        is__user_authenticated = check_user_is_authenticated(request)

        if is__user_authenticated == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            trailId = request.data['trail']
            num_users = UserInTrail.objects.filter(trail = trailId).count()
            trail = Trail.objects.get(pk = trailId)
            if num_users >= trail.maxPlayers:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            is_premium = trail.owner.plan == "Premium"
            if is_premium:
                is_valid_user = check_min_ratings(request.data['user'], trailId)
                if not is_valid_user:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer = UserInTrailSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)