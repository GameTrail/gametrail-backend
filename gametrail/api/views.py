from django.shortcuts import get_object_or_404
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
from datetime import datetime
from django.core import serializers
from rest_framework.pagination import PageNumberPagination

PLAYING = 'PLAYING'
PENDING = 'PENDING'
FINISHED = 'FINISHED'

STATUS_RECOMMENDATIONS = {
    PENDING : 1, PLAYING : 2, FINISHED : 3
}

def check_user_is_admin(request):
    user = request.user
    return user.is_staff
def check_user_is_the_same(request,usergametrail):
    user = request.user
    return user.username == usergametrail.username

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 16
    page_size_query_param = 'page_size'
    max_page_size = 16

class GetGameApiViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetGameSerializer
    queryset = Game.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['platforms__platform','genres__genre']
    pagination_class = StandardResultsSetPagination


class GetRecentGames(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetGameSerializer
    queryset = Game.objects.all().order_by("-id")[:10]
    
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
        is_user_valid = request.user.is_staff | (request.user.username == User.objects.get(pk=request.data['userId']).username)
        if is_user_valid == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = User.objects.get(pk=request.data['userId'])
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            user.delete()
            userDjango = UserDjango.objects.get(username=user.username)
            userDjango.delete()
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
                if (request.data.get("password") != None):
                    userDjango = UserDjango.objects.get(username=request.user.username)
                    userDjango.set_password(request.data.get("password"))

                    serializer.save()

                    user = User.objects.get(pk=request.data.get("userId"))
                    user.set_password(request.data.get("password"))
                    user.save()   
                             
                    userDjango.save()

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:                
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
    http_method_names = ['get']
    serializer_class = GameInListSerializer
    queryset = GameInList.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['gameList__user']

class CUGameInListApiViewSet(APIView):
    http_method_names = ['post', 'put']
    serializer_class = CUGameInListSerializer

    def post(self, request, format=None):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            userName = request.user.username
            ownerList = User.objects.get(pk = request.data['user'])
        
            if userName != ownerList.username:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                gameList = GameList.objects.get(user_id = request.data['user'])
                request.data['gameList'] = gameList.id
                serializer = CUGameInListSerializer(data = request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, format=None):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            userName = request.user.username
            ownerList = User.objects.get(pk = request.data['user'])
        
            if userName != ownerList.username:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            else:
                gameList = GameList.objects.get(user_id = request.data['user'])
                gameInList = GameInList.objects.filter(gameList_id = gameList.id, game_id = request.data['game'])[0]
                print(gameInList)
                if gameInList.gameList.id != gameList.id:
                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                
                request.data.pop("user")
                request.data["gameList"] = gameList.id

                serializer = CUGameInListSerializer(gameInList, data = request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_200_OK)
                return Response(status=status.HTTP_400_BAD_REQUEST)

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

def populate_users(request):
    result = functions.populate_users(base_json="./src/population/users/users.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of users</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 

def populate_gameLists(request):
    result = functions.populate_gameLists(base_json="./src/population/gameList/gameList.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of GameLists</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 
    return HttpResponse(html)

def populate_trails(request):
    result = functions.populate_trails(base_json="./src/population/trails/trail_copy.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of Trails</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 
    return HttpResponse(html)

def populate_comments(request):
    result = functions.populate_comments(base_json="./src/population/comments/comment.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of Comments</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 
    return HttpResponse(html)

def populate_ratings(request):
    result = functions.populate_ratings(base_json="./src/population/ratings/rating.json")
    if result:
        html = '<html><body>Database populated successfully with a lot of Ratings</body></html>'
    else:
        html = '<html><body>Database not populated<br>Maybe population is disabled.</body></html>' 
    return HttpResponse(html)

def check_user_is_authenticated(request):
    user = request.user
    return user.is_authenticated

class TrailApiViewSet(APIView):
    
    http_method_names = ['post', 'put', 'delete']
    serializer_class = TrailSerializer

    def post(self, request, format = None):
        
        if not check_user_is_authenticated(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            owner= User.objects.get(pk=request.data['owner'])
            user = request.user.username
            
            if user != owner.username:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            start_date = request.data['startDate']
            finish_date = request.data['finishDate']
            if datetime.strptime(finish_date, '%Y-%m-%d').date() < datetime.strptime(start_date, '%Y-%m-%d').date():
                return Response('La fecha de fin no puede ser anterior a la fecha de inicio!', status=status.HTTP_400_BAD_REQUEST)
        
            elif datetime.strptime(start_date, '%Y-%m-%d').date() < datetime.now().date():
                return Response('La fecha de inicio no puede ser un dia que ya ha pasado!', status=status.HTTP_400_BAD_REQUEST)
                        
            user = User.objects.get(pk=request.data['owner'])
            current_month = datetime.now().month
            trail_count = Trail.objects.filter(owner=user,creationDate__month=current_month).count()
            user.is_subscription_expired()
            if trail_count >= 1 and user.plan == "STANDARD":
                return Response('No puedes crear más de 1 trails en este mes siendo un usuario standard.', status=status.HTTP_400_BAD_REQUEST)
            maxPlayers = request.data['maxPlayers']
            if maxPlayers > 4 and user.plan == "STANDARD":
                return Response('No puedes añadir a más de 4 jugadores a tu trail siendo un usuario standard.', status=status.HTTP_400_BAD_REQUEST)
        
            serializer = PostTrailSerializer(data=request.data)
            if serializer.is_valid():
                try:
                    trail=serializer.save()
                    userInTrail = UserInTrail(user = owner, trail = trail)
                    userInTrail.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, pk=None):
        if not check_user_is_authenticated(request):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        owner = Trail.objects.get(pk=request.data['id']).owner.username
        user = request.user.username

        if user != owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            trail = Trail.objects.get(pk=request.data['id']) 
        except Trail.DoesNotExist:
            return Response('El Trail especificado no existe', status=status.HTTP_404_NOT_FOUND)

        start_date = request.data['startDate']
        finish_date = request.data['finishDate']
        if datetime.strptime(finish_date, '%Y-%m-%d').date() < datetime.strptime(start_date, '%Y-%m-%d').date():
            return Response('La fecha de fin no puede ser anterior a la fecha de inicio!', status=status.HTTP_400_BAD_REQUEST)
        
        elif datetime.strptime(start_date, '%Y-%m-%d').date() < datetime.now().date():
            return Response('La fecha de inicio no puede ser un día que ya ha pasado!', status=status.HTTP_400_BAD_REQUEST)

        serializer = PutTrailSerializer(trail, data=request.data)
        if serializer.is_valid():
            try:
                trail = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
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
    queryset = Trail.objects.all().order_by('-pk')
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields  = ['games__game','users__user']
    pagination_class = StandardResultsSetPagination


    
class RatingApiViewSet(ModelViewSet):
    http_method_names = ['get']
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
        trail = Trail.objects.get(pk=request.data['trail'])
        
        if user != owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else :
            priority = request.data['priority']
            if priority < 1 or priority > 5:
                return Response("La prioridad debe estar comprendida entre 1 y 5", status=status.HTTP_400_BAD_REQUEST)          
            serializer = GameInTrailSerializer(data=request.data)
            numJuegosTrail=trail.games.count()
            object_user = User.objects.get(username = user)
            object_user.is_subscription_expired()
            if numJuegosTrail >= 3 and object_user.plan == "STANDARD":
                return Response('No puedes añadir a más de 3 juegos a tu trail siendo un usuario standard.', status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                 serializer.save()
                 return Response(serializer.data, status=status.HTTP_201_CREATED)         
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, format = None):
        owner= Trail.objects.get(pk=request.data['trail']).owner.username
        user = request.user.username

        if user != owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                trail = GameInTrail.objects.filter(trail_id=request.data['trail'], game_id = request.data['game'])[0]
            except GameInTrail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            priority = request.data['priority']
            if priority < 1 or priority > 5:
                return Response("La prioridad debe estar comprendida entre 1 y 5", status=status.HTTP_400_BAD_REQUEST)    
            serializer = PutGameInTrailSerializer(trail, data=request.data)
            if serializer.is_valid():
                 serializer.save()
                 return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        
class POSTRatingAPIViewSet(APIView):

    http_method_names = ['post']
    serializer_class = RatingSerializer
    
    def post(self, request, format=None): 

        userWhoRate= User.objects.filter(id=request.data['userWhoRate'])
        is_user_valid = request.user.username == userWhoRate[0].username

        rating_data = request.data.get("rating", None)
        if is_user_valid:    
            if rating_data is not None and len(rating_data) <= 5:# and is_user_valid:
                
                ratings = []

                for rating_type, rating_value in rating_data.items(): 
                    rating = {
                        "ratedUser": request.data.get("ratedUser"),
                        "userWhoRate": request.data.get("userWhoRate"),
                        "rating": rating_value,
                        "type": rating_type
                    } 
                    serializer = RatingSerializer(data=rating)
                    
                    if serializer.is_valid():
                        serializer.save()
                        ratings.append(serializer.data)

                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    
                return Response(ratings, status=status.HTTP_201_CREATED)
            
            else:
                return Response({"error": "You must include between 1 and 5 ratings"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
            
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
            owner.is_subscription_expired()
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
                return Response("El trail ya está completo", status=status.HTTP_401_UNAUTHORIZED)
            trail.owner.is_subscription_expired()
            is_premium = trail.owner.plan == "Premium"
            if is_premium:
                is_valid_user = check_min_ratings(request.data['user'], trailId)
                if not is_valid_user:
                    return Response("No cumples los requisitos mínimos para entrar en este Trail con filtros Premium", status=status.HTTP_401_UNAUTHORIZED)
            userId = request.data['user']
            userintrails = UserInTrail.objects.filter(user = userId)
            time_month = datetime.now().month
            time_year = datetime.now().year
            user = User.objects.get(pk = userId)
            user.is_subscription_expired()
            count = 0
            if user.plan == "STANDARD":
                for userintrail in userintrails:
                    trail_month = userintrail.trail.startDate.month
                    trail_year = userintrail.trail.startDate.year
                    if time_month == trail_month and trail_year==time_year:
                        count +=1
                if count >= 4 :
                    return Response("Ya te has unido a 4 trails", status=status.HTTP_401_UNAUTHORIZED)
            
            
            serializer = UserInTrailSerializer(data=request.data)
            if serializer.is_valid():
                
                serializer.save()
                add_game_from_trail_to_gameList(request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
class UpdateSubscriptionAPIViewSet(ModelViewSet):
    http_method_names = ['put']
    serializer_class = UserSerializersub
    @classmethod
    
    def put(self, request, format=None):
        user_id = request.data['userId']
        action = request.data['action']
        usergametrail = User.objects.get(id=user_id)
        is_user_same = check_user_is_the_same(request,usergametrail)

        if is_user_same == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = User.objects.get(id=user_id)
                if action == 'SUBSCRIBE':
                    user.plan = 'Premium'
                    user.suscription_time =  datetime.now().date()
                elif action == 'UNSUBSCRIBE':
                    user.plan = 'STANDARD'
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
                user.save()
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            
            serializer = UserSerializersub(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

def add_game_from_trail_to_gameList(request):
    trail_id = request.data["trail"]
    user_id = request.data["user"]
    gameList_from_user = GameList.objects.filter(user = user_id)[0]
    gameList_trail = GameInTrail.objects.filter(trail = trail_id)
    for game in gameList_trail:
        gameFromTrail = game.game
        if GameInList.objects.filter(game=gameFromTrail,gameList=gameList_from_user).count()==0:
            newGame = GameInList(game = gameFromTrail,gameList=gameList_from_user,status="PENDING")
            newGame.save()

class UserTrailRecomendationViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = RecommendedTrailSerializer

    def get_queryset(self):
        username=self.request.user.username
        user = User.objects.filter(username=username)[0]
        user.is_subscription_expired()
        if user.plan != "PREMIUM":
            return []
        gamelist=GameList.objects.filter(user=user)[0]
        games=GameInList.objects.filter(gameList=gamelist)
        genres={}
        platforms={}
        for game in games:
            genresGame=Genre.objects.filter(game=game.game)
            platformsGame=Platform.objects.filter(game=game.game)
            state = game.status
            for genre in genresGame:             
                if genre.genre in genres:
                    genres[genre.genre]=genres[genre.genre] + STATUS_RECOMMENDATIONS[state]
                else:
                    genres[genre.genre]= STATUS_RECOMMENDATIONS[state]
            for platform in platformsGame:
                if platform.platform in platforms:
                    platforms[platform.platform]=platforms[platform.platform] + STATUS_RECOMMENDATIONS[state]
                else:
                    platforms[platform.platform]= STATUS_RECOMMENDATIONS[state]
        sortedGenres=sorted(genres.items(), key=lambda x:x[1])
        sortedPlatforms=sorted(platforms.items(), key=lambda x:x[1])
        genresFinal=sortedGenres[-3:]
        platformsFinal=sortedPlatforms[-2:]
        gameInTrails=GameInTrail.objects.filter(game__genres__genre__in=dict(genresFinal).keys(), game__platforms__platform__in=dict(platformsFinal).keys()).distinct()
        trails = Trail.objects.filter(games__in = gameInTrails).distinct()[:9]
        return trails