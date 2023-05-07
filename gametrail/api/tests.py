from django.test import TestCase
from gametrail.api.views import GameInTrailViewSet, GetTrailApiViewSet, TrailApiViewSet, UserApiViewSet, POSTRatingAPIViewSet, CreateMinRatingViewSet, GetMinRatingTrailApiViewSet, AddUserInTrailViewSet
from gametrail.models import Game, GameInTrail, Rating, User, MinRatingTrail, Trail, UserInTrail
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
import secrets
import string

ALPHABET = string.ascii_letters + string.digits
PASSWORD = ''.join(secrets.choice(ALPHABET) for i in range(20))
