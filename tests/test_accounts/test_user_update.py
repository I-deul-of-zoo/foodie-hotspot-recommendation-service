import json
import pytest

from django.core.cache import cache


@pytest.mark.django_db
def test_user_check(client, access_token):
    # # 직접 생성하는 경우에는... 잘 안되네
    # # user = User.objects.create(username='testuser1', password='devpassword&*')
    
    # # 유저 회원가입
    # signup_url = "/api/auth/signup"
    # data = {"username": "testuser1", "password": "devpassword&*"}
    # response = client.post(signup_url,
    #             data=json.dumps(data),
    #             content_type="application/json")
    
    # assert response.status_code == 201
    
    # # 유저 토큰
    # login_url = "/api/auth/jwt-login"
    # data = {"username": "testuser1", "password": "devpassword&*"}
    # response = client.post(login_url,
    #             data=json.dumps(data),
    #             content_type="application/json")
    
    # assert response.status_code == 200
    # assert response.json().get("access_token") != None

    # # 초기 유저정보 확인
    # access_token = response.json().get("access_token")
    url = "/api/account/"
    response = client.get(url,
                        headers={"Authorization": f"Bearer {access_token}"},
                        content_type="application/json")
    
    assert response.status_code == 200
    
    latitude = response.data.get("latitude")
    longitude = response.data.get("longitude")
    is_recommend = response.data.get("is_recommend")
    assert latitude == ""
    assert longitude == ""
    assert is_recommend == False

def test_user_update(client, access_token):  
    # 유저 정보 변경 후 체크
    expected = {
        "latitude": "100.1234",
        "longitude": "200.1234",
        "is_recommend": True,
    }
    
    url = "/api/account/"
    response = client.put(url,
                        headers={"Authorization": f"Bearer {access_token}"},
                        data=json.dumps(expected),
                        content_type="application/json")
    
    assert response.status_code == 200
    latitude = response.data.get("latitude")
    longitude = response.data.get("longitude")
    is_recommend = response.data.get("is_recommend")
    assert expected.get("latitude") == latitude
    assert expected.get("longitude") == longitude
    assert expected.get("is_recommend") == is_recommend
    