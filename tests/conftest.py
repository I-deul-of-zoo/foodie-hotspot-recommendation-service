import pytest
import jwt
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.test import APIClient
from foodiehotspots.models import Restaurant
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="testpassword",
    )

@pytest.fixture
def access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

@pytest.fixture
def create_restaurant():
    return mixer.blend(Restaurant)


# @pytest.fixture
# def create_rate(create_user, create_restaurant):
#     def _create_rate(user=None, restaurant=None, score=3, content="Test content"):
#         if user is None:
#             user = create_user()
#         if restaurant is None:
#             restaurant = create_restaurant()
#         return Rate.objects.create(user=user, restaurant=restaurant, score=score, content=content)
#     return _create_rate

'''
1. 테스트db에 csv 더미를 넣음 (레스토랑 생성 안함)
2. 유저, 토큰 -> conf 생성
3. 
'''