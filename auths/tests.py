from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


class AuthsTests(APITestCase):
    def setUp(self):
        # 테스트용 유저 생성
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        
    def test_signup(self):
        # 회원가입 테스트
        url = reverse("auths:signup")
        data = {
            'username': 'newuser',
            'password': 'newpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')

    def test_jwt_login(self):
        # JWT 로그인 테스트
        url =reverse("auths:jwt-login")
        data = {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertEqual(response.data['username'], self.user_data['username'])
