from django.test import TestCase
from gametrail.api.Trail.views import GameInTrailViewSet, GetTrailApiViewSet, TrailApiViewSet, UserApiViewSet, POSTRatingAPIViewSet, CreateMinRatingViewSet, GetMinRatingTrailApiViewSet, AddUserInTrailViewSet
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

