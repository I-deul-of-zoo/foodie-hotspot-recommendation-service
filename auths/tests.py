import pytest, sys, logging
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


    
@pytest.mark.django_db
class TestAuthsClass():
    def setup_method(self):
        # 테스트용 유저 생성
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.client = APIClient()
        logging.info(sys._getframe(0).f_code.co_name)

    def test_signup(self):
        # 회원가입 테스트
        url = reverse("auths:signup")
        data = {
            'username': 'newuser',
            'password': 'newpassword',
        }
        logging.info(sys._getframe(0).f_code.co_name)
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data

    def test_jwt_login(self):
        # JWT 로그인 테스트
        url = reverse("auths:jwt-login")
        data = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        }
        logging.info(sys._getframe(0).f_code.co_name)
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data
        assert response.data['username'] == self.user_data['username']

