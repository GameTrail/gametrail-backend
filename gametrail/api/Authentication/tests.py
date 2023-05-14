from django.test import TestCase
from gametrail.api.Trail.views import GameInListApiViewSet,CUGameInListApiViewSet,GameInTrailViewSet, GetTrailApiViewSet, TrailApiViewSet, UserApiViewSet, POSTRatingAPIViewSet, CreateMinRatingViewSet, GetMinRatingTrailApiViewSet, AddUserInTrailViewSet
from gametrail.models import Game, GameInTrail, Rating, User, MinRatingTrail, Trail, UserInTrail
from gametrail.api.tests import *
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
import secrets
import string

class RatingApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.ratedUser = User.objects.create_user(username='miguelito', email='miguel_mola@gmail.com' ,avatar='kajnfawkef.jpg' ,password=PASSWORD)
        self.userWhoRate = User.objects.create_user(username='pedrito', email='pedritodestroza@gmail.com' ,avatar='sfsfsfdsf.jpg' ,password=PASSWORD)

        self.ratedUser_id = self.ratedUser.pk
        self.userWhoRate_id = self.userWhoRate.pk

        self.rating_kindness = Rating.objects.create(
                                            rating = 1, 
                                            type ='KINDNESS',
                                            ratedUser = self.ratedUser,
                                            userWhoRate = self.userWhoRate)
        
        self.rating_kindness = Rating.objects.create(
                                    rating = 2, 
                                    type ='KINDNESS',
                                    ratedUser = self.ratedUser,
                                    userWhoRate = self.ratedUser)
        
        self.url_rating = '/api/rating' 
        self.url_user = '/api/user/'

    def test_get_ratings(self):
    
        request = self.factory.get(self.url_user + str(self.ratedUser_id) )
        view = UserApiViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['average_ratings']['KINDNESS'], 1.5)

    def test_post_wrong_type(self):
       
        data = {
            'rating': {
                "KINDNES": 1
            },
            'ratedUser': '2',
            'userWhoRate': '1'  
        }

        request = self.factory.post(self.url_rating, data, format='json')
        force_authenticate(request, self.ratedUser)
        
        view = POSTRatingAPIViewSet.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['type'][0], "\"KINDNES\" is not a valid choice.")

    def test_post_not_authenticated(self):
       
        data = {
            'rating': {
                "KINDNESS": 1
            },
            'ratedUser': '2',
            'userWhoRate': '1'  
        }

        request = self.factory.post(self.url_rating, data, format='json')
        
        view = POSTRatingAPIViewSet.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post(self):
       
        data = {
            'rating': {
                "AVAILABILITY": '1'
            },
            'ratedUser': '1',
            'userWhoRate': '2'  
        }

        request = self.factory.post(self.url_rating, data, format='json')
        force_authenticate(request, self.userWhoRate)
        
        view = POSTRatingAPIViewSet.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request = self.factory.get(self.url_user + str(self.userWhoRate_id) )
        view = UserApiViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['average_ratings']['AVAILABILITY'], 1)

class MinRatingApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.premiumUser = User.objects.create_user(username='miguelito', email='miguel_mola@gmail.com' ,avatar='kajnfawkef.jpg' ,password=PASSWORD)
        self.premiumUser.plan = "Premium"
        self.premiumUser.save()
        self.standartUser = User.objects.create_user(username='pedrito', email='pedritodestroza@gmail.com' ,avatar='sfsfsfdsf.jpg' ,password=PASSWORD)

        self.premiumUser_id = self.premiumUser.pk
        self.standartUser_id = self.standartUser.pk

        self.trail = Trail.objects.create(owner=self.premiumUser, 
                                            name='Test Trail 1',
                                            description='Test Trail 1',
                                            startDate='2023-04-12',
                                            maxPlayers='2', 
                                            finishDate='2023-04-15')
        
        
        self.min_rating = MinRatingTrail.objects.create(
                                                        minRating = 2, 
                                                        ratingType ='KINDNESS',
                                                        trail = self.trail,
                                                        user = self.premiumUser)
        
        self.url_rating = '/api/minRating/' 
        self.url_create_rating = '/api/createMinRating'
        self.url_add_user = '/api/addUserInTrail'

    def test_get_ratings(self):
    
        request = self.factory.get(self.url_rating)
        view = GetMinRatingTrailApiViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['ratingType'], 'KINDNESS')

    def test_post_not_premium(self):
       
        data = {
            'ratingType': 'KINDNESS',
            'minRating': '1',
            'trail': '1',
            'user': '2'  
        }

        request = self.factory.post(self.url_create_rating, data, format='json')
        force_authenticate(request, self.standartUser)
        
        view = CreateMinRatingViewSet.as_view()
        response = view(request)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post(self):
       
        data = {
            'ratingType': 'AVAILABILITY',
            'minRating': '1',
            'trail': '1',
            'user': '1'  
        }

        request = self.factory.post(self.url_create_rating, data, format='json')
        force_authenticate(request, self.premiumUser)
        
        view = CreateMinRatingViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_add_user = {
            'trail': '1',
            'user': '2'  
        }

        request = self.factory.post(self.url_add_user, data_add_user, format='json')
        force_authenticate(request, self.standartUser)
        view = AddUserInTrailViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.url_gameList_user = '/api/gameList/?gameList__user='


    #Test añadir juego a gameList con usuario no autenticado
    def test_post_gameList_not_authenticated(self):    

        data = {'user' : '1','game': self.game_id,'status':'PENDING'}
        request = self.factory.post(self.url_gameList_game,data,format='json')

        view =  CUGameInListApiViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #Test añadir juego a gameList propia con usuario de gameList autenticado
    def test_post_own_gameList_authenticated(self):

        data = {'user' : self.userGameList_id,'game': self.game_id,'status':'PENDING'}
        request = self.factory.post(self.url_gameList_game,data,format='json')
        force_authenticate(request, self.userGameList)

        view =  CUGameInListApiViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #Test editar estado juego a gameList con usuario no autenticado
    def test_put_gameList_not_authenticated(self):  
        
        data = {'user' : self.userGameList_id,'game': self.game_id,'status':'PLAYING'}
        request = self.factory.put(self.url_gameList_game,data,format='json')

        view =  CUGameInListApiViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    #Test editar estado juego a gameList con usuario autenticado
    def test_put_gameList_authenticated(self):        
        
        data1 = {'user' : self.userGameList_id,'game': self.game_id,'status':'PENDING'}
        request1 = self.factory.post(self.url_gameList_game,data1,format='json')
        force_authenticate(request1, self.userGameList)

        view1 =  CUGameInListApiViewSet.as_view()
        response1 = view1(request1)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)


        data2 = {'user' : self.userGameList_id,'game': self.game_id,'status':'PLAYING'}
        request2 = self.factory.put(self.url_gameList_game,data2,format='json')
        force_authenticate(request2, self.userGameList)
        
        view2 =  CUGameInListApiViewSet.as_view()
        response2= view2(request2)

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    #Test ver gamelist de un usuario
    def test_get_gameList(self): 
        request = self.factory.get(self.url_gameList_user + str(self.userGameList_id))
        view = GameInListApiViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
