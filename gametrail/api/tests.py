from django.test import TestCase
from gametrail.api.views import UserApiViewSet, POSTRatingAPIViewSet
from gametrail.models import Rating, User
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate



class RatingApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.ratedUser = User.objects.create_user(username='miguelito', email='miguel_mola@gmail.com' ,avatar='kajnfawkef.jpg' ,password='miguelmolamucho')
        self.userWhoRate = User.objects.create_user(username='pedrito', email='pedritodestroza@gmail.com' ,avatar='sfsfsfdsf.jpg' ,password='pedroteodia')

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