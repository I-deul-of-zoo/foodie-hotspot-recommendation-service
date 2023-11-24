import pytest
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def user():
    user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
    user = get_user_model().objects.create_user(**user_data)
    
    return user


@pytest.fixture
def access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
