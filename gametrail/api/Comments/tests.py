from django.test import TestCase
from gametrail.api.Comments.views import *
from gametrail.models import Game, User, Comment
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
import secrets
import string
from gametrail.api.tests import *

class CommentApiViewSetTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create_user(username='prueba1', email='prueba1@gmail.com' ,avatar='pruebaIM.jpg' ,password=PASSWORD)
        self.user2 = User.objects.create_user(username='prueba2', email='prueba2@gmail.com' ,avatar='pruebaIM2.jpg' ,password=PASSWORD)

        self.game= Game.objects.create(name= 'juego prueba 1',
                                       releaseDate='2023-05-14',
                                       image='rguwvnuwnv.jpg',
                                       photos='jaervrvrvrv.jpg',
                                       description='prueba descripcion')
        
        self.comment1 = Comment.objects.create(commentText = 'comentario de prueba usuario', userWhoComments = self.user1, 
                                               userCommented = self.user2)
        
        self.comment2 = Comment.objects.create(commentText = 'comentario de prueba juego', userWhoComments = self.user1, 
                                               game = self.game)
        
        self.url1 = '/api/comment/user' 
        self.url2 = '/api/comment/game'
        self.url3 = '/api/comment' 

    def test_get_comment_user(self):
        
        request = self.factory.get(self.url1, {'user_id': self.user2.id})
        view = CommentsByUserId.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_comment_game(self):
        
        request = self.factory.get(self.url2, {'game_id': self.game.id})
        view = GameCommentAPIView.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_post_comment_user(self):

        data_add_comment = {
            'commentText' : 'texto de prueba',
            'userWhoComments' : self.user1.pk,
            'userCommented' : self.user2.pk
        }

        request = self.factory.post(self.url3, data_add_comment)
        force_authenticate(request, user=self.user1)
        view = CUDCommentsAPIViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request2 = self.factory.get(self.url1, {'user_id': self.user2.id})
        view = CommentsByUserId.as_view({'get': 'list'})
        response2 = view(request2)
        self.assertEqual(len(response2.data), 2)

    def test_post_comment_game(self):

        data_add_comment = {
            'commentText' : 'texto de prueba',
            'userWhoComments' : self.user1.pk,
            'game' : self.game.pk
        }

        request = self.factory.post(self.url3, data_add_comment)
        force_authenticate(request, user=self.user1)
        view = CUDCommentsAPIViewSet.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request2 = self.factory.get(self.url2, {'game_id': self.game.id})
        view = GameCommentAPIView.as_view({'get': 'list'})
        response2 = view(request2)
        self.assertEqual(len(response2.data), 2)

