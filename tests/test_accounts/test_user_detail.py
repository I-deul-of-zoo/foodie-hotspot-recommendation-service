import pytest, sys, logging
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

#사용자 정보가져오기 API 테스트
@pytest.mark.django_db
class TestUserDetailClass:
    url = reverse('accounts:user-detail')
    def test_patch_userdetail(self, client, access_token)    :
        logging.info(sys._getframe(0).f_code.co_name)
        data = {
            "latitude":"1.61804",
            "longitude":"3.14159",
        }
        response = client.patch(self.url, 
            headers={"Authorization": f"Bearer {access_token}"},
            content_type="application/json",
            data=data)
        assert response.status_code == 200        
        
        
    def test_get_userdetail(self, client,access_token):
        logging.info(sys._getframe(0).f_code.co_name)
        response = client.get(self.url, 
            headers={"Authorization": f"Bearer {access_token}"},
            content_type="application/json")
        
        assert response.status_code == 200
        assert 'password' not in response.data
    