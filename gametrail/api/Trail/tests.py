from django.test import TestCase
from gametrail.api.Trail.views import GameInTrailViewSet, GetTrailApiViewSet, TrailApiViewSet, UserApiViewSet, POSTRatingAPIViewSet, CreateMinRatingViewSet, GetMinRatingTrailApiViewSet, AddUserInTrailViewSet
from gametrail.models import Game, GameInTrail, Rating, User, MinRatingTrail, Trail, UserInTrail
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
import secrets
import string
from gametrail.api.tests import *


#TESTS PARA TRAILS
class TrailApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(userName='Juanan1', email='juanan@gmail.com' ,avatar='kajnfawkef.jpg' ,password=PASSWORD)

        self.user2 = User.objects.create_user(userName='Juanan2', email='juanan2@gmail.com' ,avatar='kajnfawkef.jpg' ,password=PASSWORD)

        self.trail1 = Trail.objects.create(owner=self.user, 
                                            name='Test Trail 1',
                                            description='Test Trail 1',
                                            startDate='2023-04-12',
                                            maxPlayers='2', 
                                            finishDate='2023-04-15')
        self.game= Game.objects.create( name= 'Juego 1',
                                       releaseDate='2023-04-17',
                                       image='akhugfdkaw.jpg',
                                       photos='jgfyhae.jpg',
                                       description='holaaaaaa')
        
        self.url = '/api/getTrail/' 
        self.url1 = '/api/trail/' 
        self.url2= 'api/gameInTrail'
        self.url3 = '/api/addUserInTrail'

    def test_get_trails(self):
    
        request = self.factory.get(self.url)
        view = GetTrailApiViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


    def test_post_trail(self):
       
        data = {
            'owner': self.user.id,
            'name': 'Test Trail 2',
            'startDate': '2023-04-17',
            'finishDate': '2023-04-19',
            'description': 'HOLAA',
            'maxPlayers': '3',
        }
        request = self.factory.post(self.url1, data)
        force_authenticate(request, self.user)
        
        view = TrailApiViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_post_invalid_trail(self):

        #Fecha Inválida
        data = {
            'owner': self.user.id,
            'name': 'Test Trail 2',
            'startDate': '2023-04-17',
            'finishDate': '2023-04-16',
            'description': 'HOLAA',
            'maxPlayers': '3',
        }
        request = self.factory.post(self.url1, data)
        force_authenticate(request, self.user)
        
        view = TrailApiViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_game_trail(self):

        data_add_game={
            'game': self.game.id,
            'trail':self.trail1.id,
            'message':'holaa',
            'priority': 2,
            'status':'PLAYING'
        }

        request = self.factory.post(self.url2, data_add_game, format='json')
        force_authenticate(request, self.user)
        view = GameInTrailViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        trail = GameInTrail.objects.get(pk=self.game.id)
        self.assertEqual(trail.message, 'holaa')


    def test_post_unauthorized_game_trail(self):
        data_add_game={
            'game': self.game.id,
            'trail':self.trail1.id,
            'message':'holaa',
            'priority': 2,
            'status':'PLAYING'
        }

        request = self.factory.post(self.url2, data_add_game, format='json')
        force_authenticate(request, self.user2)
        view = GameInTrailViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_post_user_trail(self):

        data_add_user={
            'trail': self.trail1.id,
            'user': self.user2.id
        }

        request = self.factory.post(self.url3, data_add_user, format='json')
        force_authenticate(request, self.user)
        view = AddUserInTrailViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        trail = UserInTrail.objects.get(pk=self.trail1.id)
        self.assertEqual(trail.user.id, 2)
  

    def test_post_user_invalid_trail(self):
       
        data_add_user={
            'trail': self.trail1.id,
            'user': '6' 
        }

        request = self.factory.post(self.url3, data_add_user, format='json')
        force_authenticate(request, self.user)
        view = AddUserInTrailViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       

    def test_put_trail(self):
        data = {
            'id' : self.trail1.id,
            'name': 'wdadawdawdddddd',
            'description' : 'EYEYEY',
            'startDate':'2023-04-22',
            'finishDate':'2023-04-24',
            'maxPlayers': '3',
            'owner': self.user.id
        }
        request = self.factory.put(self.url1, data)
        force_authenticate(request, self.user)
        view = TrailApiViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
       
        trail = Trail.objects.get(pk=self.trail1.id)
        self.assertEqual(trail.name, 'wdadawdawdddddd')


    def test_put_game_trail(self):

        data_add_game={
            'game': self.game.id,
            'trail':self.trail1.id,
            'message':'holaa',
            'priority': 2,
            'status':'PLAYING'
        }

        request = self.factory.post(self.url2, data_add_game, format='json')
        force_authenticate(request, self.user)
        view = GameInTrailViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        trail = GameInTrail.objects.get(pk=self.game.id)
        self.assertEqual(trail.message, 'holaa')


        data_put_game={
            'game': self.game.id,
            'trail':self.trail1.id,
            'message':'prueba1',
            'priority': 2,
            'status':'PLAYING'
        }

        request = self.factory.put(self.url2, data_put_game, format='json')
        force_authenticate(request, self.user)
        view = GameInTrailViewSet.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        trail = GameInTrail.objects.get(pk=self.game.id)
        self.assertEqual(trail.message, 'prueba1')
        