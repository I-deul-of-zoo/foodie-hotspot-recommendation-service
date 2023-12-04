import json
import pytest

from foodiehotspots.models import Restaurant
from foodiehotspots.serializers import FoodieDetailsSerializers


# @pytest.mark.django_db
def test_restaurant_detail(client, access_db, access_token, create_dummy_restaurant):
    
    # 레스토랑 상세정보?
    rest_pk = 1
    expected = Restaurant.objects.get(pk=rest_pk)
    assert expected
    
    #값만 비교하면 되지 않나? serializer로 만든 이유는?
    # API로 가져온 상세정보와 기대값 비교하여 일치 확인
    serializer = FoodieDetailsSerializers(expected)
    expected_data = serializer.data
    url = f"/api/restaurant/{rest_pk}"
    response = client.get(url, 
                        headers={"Authorization": f"Bearer {access_token}"},content_type="application/json")
        
    assert response.status_code == 200
    
    ## 비교하기 위해 데이터 변형
    ## QuerySet은 직접 비교가 되지 않습니다.
    expected_data['related_eval_ids'] = list(expected_data['related_eval_ids'])
    response.data['related_eval_ids'] = list(response.data['related_eval_ids'])
    
    ## 다른 객체이지만 내용물은 모두 같습니다.
    ## dict와 list는 직접 비교해도 내용물까지 같은지 확인합니다.
    assert id(dict(expected_data)) != id(dict(response.data))
    assert dict(expected_data) == dict(response.data)



# @pytest.fixture(scope="function")
# def create_testuser_get_token(client, access_db):
#     # 유저 회원가입
#     signup_url = "/api/auth/signup"
#     data = {"username": "testuser1", "password": "devpassword&*"}
#     response = client.post(signup_url,
#                 data=json.dumps(data),
#                 content_type="application/json")
    
#     assert response.status_code == 201
    
#     # 유저 토큰
#     login_url = "/api/auth/jwt-login"
#     data = {"username": "testuser1", "password": "devpassword&*"}
#     response = client.post(login_url,
#                 data=json.dumps(data),
#                 content_type="application/json")
    
#     assert response.status_code == 200
#     assert response.json().get("access_token")
    
#     return response.json().get("access_token")
    
# def test_get_location(client, access_token, access_db, create_locations):
#     # 직접 생성하는 경우에는... 잘 안되네
#     # user = User.objects.create(username='testuser1', password='devpassword&*')
    
#     # 초기 유저정보 확인
#     url = "/api/account/"
#     response = client.get(url,
#                           headers={"Authorization": f"Bearer {access_token}"},
#                           content_type="application/json")
    
#     assert response.status_code == 200
    
#     latitude = response.data.get("latitude")
#     longitude = response.data.get("longitude")
#     is_recommend = response.data.get("is_recommend")
#     assert latitude == ""
#     assert longitude == ""
#     assert is_recommend == False
    
    
#     # Locations
#     expected = {"dosi": "강원", "sgg": "강릉시"}
#     url = f"/api/account/locations/?dosi={expected.get('dosi')}&sgg={expected.get('sgg')}"
#     response = client.get(url, 
#                           headers={"Authorization": f"Bearer {access_token}"},content_type="application/json")

#     assert response.status_code == 200
#     assert response.data.get("count") == 1
#     assert response.data.get("next") == None
#     assert response.data.get("previous") == None
    
#     results = response.data.get("results") # 한 개 있어도 list로 반환됨
#     result = results[0]
    
#     assert result.get("dosi") == expected.get("dosi")
#     assert result.get("sgg") == expected.get("sgg")

