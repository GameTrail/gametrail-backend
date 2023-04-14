from django.test import TestCase
from gametrail.api.views import RatingApiViewSet
from gametrail.models import Rating, User
from rest_framework.test import APIRequestFactory
from rest_framework import status



class RatingApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.ratedUser = User.objects.create_user(username='miguelito', email='miguel_mola@gmail.com' ,avatar='kajnfawkef.jpg' ,password='miguelmolamucho')
        self.userWhoRate = User.objects.create_user(username='pedrito', email='pedritodestroza@gmail.com' ,avatar='sfsfsfdsf.jpg' ,password='pedroteodia')

        self.rating_kindness = Rating.objects.create(
                                            rating = 1, 
                                            type ='KINDNESS',
                                            ratedUser = self.ratedUser,
                                            userWhoRate = self.userWhoRate)
        
        self.url_rating = '/api/rating' 
        self.url_user = '/api/user/' 

    def test_get_ratings(self):
    
        request = self.factory.get(self.url_user)
        view = RatingApiViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # def test_get_trail_id(self):
        
    #     request = self.factory.get(f'{self.url}{self.trail1.id}/')
        
    #     view = GetTrailApiViewSet.as_view({'get': 'retrieve'})
    #     response = view(request, pk=self.trail1.id)
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['name'], 'Test Trail 1') 

    # def test_post_invalid_data(self):
       
    #     data = {
    #         'owner': self.owner.id,
    #         'name': 'Test Trail 2',
    #         'startDate': '2023-04-15',
    #         'finishDate': '2023-04-13'  
    #     }
    #     request = self.factory.post(self.url1, data)
    #     request.user = self.user
        
    #     view = TrailApiViewSet.as_view()
    #     response = view(request)
        
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertEqual(Trail.objects.count(), 1) 