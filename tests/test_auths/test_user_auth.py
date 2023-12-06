import pytest, sys, logging
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

@pytest.mark.django_db
class TestAuthsClass():

    def test_signup(self, client):
        # 회원가입 테스트
        url = reverse("auths:signup")
        data = {
            'username': 'newuser',
            'password': 'newpassword',
        }
        logging.info(sys._getframe(0).f_code.co_name)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data

    def test_jwt_login(self, client, user, user_data):
        
        # JWT 로그인 테스트
        url = reverse("auths:jwt-login")
        data = {
            'username': user_data["username"],
            'password': user_data["password"],
        }
        logging.info(sys._getframe(0).f_code.co_name)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data
        assert response.data['username'] == user_data["username"]