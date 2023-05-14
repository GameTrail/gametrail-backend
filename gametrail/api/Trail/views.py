from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from gametrail import functions
from django.db.models import Avg
from gametrail.models import *
from gametrail.api.serializers import *
from gametrail.api.Game.views import *
from gametrail.api.Authentication.views import *
from gametrail.api.Comments.views import *
from gametrail.api.Trail.trailSerializers import *
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
import django_filters
from django_filters import rest_framework as filters

PLAYING = 'PLAYING'
PENDING = 'PENDING'
FINISHED = 'FINISHED'

STATUS_RECOMMENDATIONS = {
    PENDING : 1, PLAYING : 2, FINISHED : 3
}

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
            if int(maxPlayers) > 4 and user.plan == "STANDARD":
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
        owner= Trail.objects.get(pk=request.data['trailId']).owner.username
        user = request.user.username
        if user != owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                trail = Trail.objects.get(pk=request.data['trailId'])
            except Trail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            trail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class TrailFilter(filters.FilterSet):
    created_before = filters.DateFilter(field_name='creationDate', lookup_expr='lte')
    created_after = filters.DateFilter(field_name='creationDate', lookup_expr='gte')
    started_before = filters.DateFilter(field_name='startDate', lookup_expr='lte')
    started_after = filters.DateFilter(field_name='startDate', lookup_expr='gte')
    finished_before = filters.DateFilter(field_name='finishDate', lookup_expr='lte')
    finished_after = filters.DateFilter(field_name='finishDate', lookup_expr='gte')
    game_name = django_filters.CharFilter(field_name='games__game__name', lookup_expr='icontains')
    user_name = django_filters.CharFilter(field_name='users__user__username', lookup_expr='icontains')   
    platform = django_filters.CharFilter(field_name='platforms__platform', lookup_expr='icontains')   

    class Meta:
        model = Trail
        fields = ['created_before', 'created_after','started_before', 'started_after','finished_before', 'finished_after','games__game','users__user','game_name', 'user_name', 'platform']
class GetTrailApiViewSet(ModelViewSet):
    
    http_method_names = ['get']
    serializer_class = TrailSerializer
    queryset = Trail.objects.all().order_by('-pk')
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_class = TrailFilter
    pagination_class = StandardResultsSetPagination
    
class GetMinRatingTrailApiViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = GetMinRatingTrailSerializer
    queryset = MinRatingTrail.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields  = ['trail']

class GameInTrailViewSet(APIView):
    http_method_names = ['post', 'put','delete']
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
        
    def delete(self, request, format = None):
        owner= Trail.objects.get(pk=request.data['trailId']).owner.username
        user = request.user.username
        if user != owner:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
               trail = GameInTrail.objects.filter(trail_id=request.data['trailId'], game_id = request.data['gameToDelete'])[0]
            except Trail.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if trail.status != 'PENDING':
                return Response("Deberia estar el trail en pending", status=status.HTTP_400_BAD_REQUEST)
            
            
            trail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
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
        
class UserAdvancedTrailRecomendationViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = RecommendedTrailSerializer

    def get_queryset(self):
        is__user_authenticated = check_user_is_authenticated(self.request)

        if is__user_authenticated == False:
            return []
        username=self.request.user.username
        user = User.objects.filter(username=username)[0]
        user.is_subscription_expired()
        if user.plan != "Premium":
            return []
        trails = sorted(Trail.objects.all(), key=lambda x:-x.average_ratings)[:10]
        return trails

class UserTrailRecomendationViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = RecommendedTrailSerializer

    def get_queryset(self):
        is__user_authenticated = check_user_is_authenticated(self.request)

        if is__user_authenticated == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
    
class GameListImageIA(APIView):
    http_method_names = ['post']
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
                try:
                    image = request.data['image']
                    list_games_to_add = functions.tesseract_image_read(image)
                    dgameList = GameList.objects.get(user_id = request.data['user'])
                    try:
                        for dgame in list_games_to_add:
                            if dgame != None:
                                #print(dgame.id)
                                newGame = GameInList.objects.create(
                                    game = dgame, gameList = dgameList, status = "PENDING"
                                )
                                newGame.save()
                        return Response(str(len(list_games_to_add)) + " games added to list. " + str(list_games_to_add), status = status.HTTP_201_CREATED)
                    except:
                        return Response("Some games were already in list",status=status.HTTP_200_OK)

                except:            
                    return Response("Image was not read properly", status=status.HTTP_400_BAD_REQUEST)

class GetTrailPatrocinedViewSet(ModelViewSet):
    http_method_names = ['get']
    serializer_class = TrailPatrocinedSerializer
    queryset = TrailPatrocinado.objects.all()

class CTrailPatrocinedViewSet(APIView):
    http_method_names = ['post', 'put']
    serializer_class = CTrailPatrocinedSerializer

    def post(self, request, format = None):
        is_user_admin = check_user_is_admin(request)

        if is_user_admin == False:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            trailsPatrocinados = TrailPatrocinado.objects.all()
            if len(trailsPatrocinados) == 1:
                return Response("Ya existe un Trail Patrocinado creado. Modificalo con un método PUT", status=status.HTTP_400_BAD_REQUEST)

            serializer = CTrailPatrocinedSerializer(data=request.data)

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
                trail = TrailPatrocinado.objects.get(pk=1)
            except TrailPatrocinado.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = CTrailPatrocinedSerializer(trail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   