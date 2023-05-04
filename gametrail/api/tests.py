from django.test import TestCase
from gametrail.api.views import GameInTrailViewSet, GetTrailApiViewSet, TrailApiViewSet, UserApiViewSet, POSTRatingAPIViewSet, CreateMinRatingViewSet, GetMinRatingTrailApiViewSet, AddUserInTrailViewSet, CUGameInListApiViewSet
from gametrail.models import Game, GameInTrail, Rating, User, MinRatingTrail, Trail, UserInTrail, GameList
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
import secrets
import string

ALPHABET = string.ascii_letters + string.digits
PASSWORD = ''.join(secrets.choice(ALPHABET) for i in range(20))

#TEST PARA GAMELIST
class GameListApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        #Usuario
        self.userGameList = User.objects.create_user(username='pruebaGameList1', email='pruebagamelist@gmail.com' ,avatar='avatar.jpg' ,password=PASSWORD)
        self.userGameList_id =  self.userGameList.pk

        #Juego
        self.game= Game.objects.create( name= 'Juego Game List',releaseDate='2022-04-10',image='juegoPrueba1.jpg',photos='juegoPruebaGameList.jpg', description='lore ipsum')
        self.game_id =  self.game.pk

        #URL
        self.url_gameList_game = '/api/gameList/game'


    #Test añadir juego a gameList con usuario no autenticado
    def test_post_gameList_not_authenticated(self):    

        data = {'user' : '1','game': '1','status':'PENDING'}
        request = self.factory.post(self.url_gameList_game,data,format='json')

        view =  CUGameInListApiViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #Test añadir juego a gameList propia con usuario de gameList autenticado
    def test_post_own_gameList_authenticated(self):

        data = {'user' : '1','game': '1','status':'PENDING'}
        request = self.factory.post(self.url_gameList_game,data,format='json')
        force_authenticate(request, self.userGameList)

        view =  CUGameInListApiViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #Test editar estado juego a gameList con usuario no autenticado
    def test_put_gameList_not_authenticated(self):  
        
        data = {'user' : '1','game': '1','status':'PLAYING'}
        request = self.factory.put(self.url_gameList_game,data,format='json')

        view =  CUGameInListApiViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #Test editar estado juego a gameList con usuario autenticado
    def test_put_gameList_authenticated(self):        
    
        data = {'user' : '1','game': '1','status':'PLAYING'}
        request = self.factory.put(self.url_gameList_game,data,format='json')
        force_authenticate(request, self.userGameList)
        
        view =  CUGameInListApiViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

