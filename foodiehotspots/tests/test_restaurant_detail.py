import json
import pytest

from foodiehotspots.models import Restaurant
from foodiehotspots.serializers import FoodieDetailsSerializers


@pytest.fixture(scope="function")
def access_db(db):
    pass

@pytest.fixture(scope="function")
def create_locations(access_db):
    from utils.location import location_load
    location_load.load_to_db()
    
@pytest.fixture(scope="function")
def create_dummy_restaurant(access_db):
    import csv
    from foodiehotspots.models import Restaurant
    with open("./utils/restaurant_test_data.csv", "r", encoding="utf-8-sig") as f:
        csv_to_list = list(csv.DictReader(f))

        for i, row in enumerate(csv_to_list):
            row["name_address"] = row["name"] + row["address_roadnm"] + row["address_lotno"]
            print(row)
            Restaurant.objects.create(**row)
            # temp.save()

@pytest.fixture(scope="function")
def create_testuser_get_token(client, access_db):
    # 유저 회원가입
    signup_url = "/api/auth/signup"
    data = {"username": "testuser1", "password": "devpassword&*"}
    response = client.post(signup_url,
                data=json.dumps(data),
                content_type="application/json")
    
    assert response.status_code == 201
    
    # 유저 토큰
    login_url = "/api/auth/jwt-login"
    data = {"username": "testuser1", "password": "devpassword&*"}
    response = client.post(login_url,
                data=json.dumps(data),
                content_type="application/json")
    
    assert response.status_code == 200
    assert response.json().get("access_token")
    
    return response.json().get("access_token")
    
def test_get_location(client, create_testuser_get_token, access_db, create_locations):
    # 직접 생성하는 경우에는... 잘 안되네
    # user = User.objects.create(username='testuser1', password='devpassword&*')
    
    # 초기 유저정보 확인
    access_token = create_testuser_get_token
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
    
    
    # Locations
    expected = {"dosi": "강원", "sgg": "강릉시"}
    url = f"/api/account/locations/?dosi={expected.get('dosi')}&sgg={expected.get('sgg')}"
    response = client.get(url, 
                          headers={"Authorization": f"Bearer {access_token}"},content_type="application/json")

    assert response.status_code == 200
    assert response.data.get("count") == 1
    assert response.data.get("next") == None
    assert response.data.get("previous") == None
    
    results = response.data.get("results") # 한 개 있어도 list로 반환됨
    result = results[0]
    
    assert result.get("dosi") == expected.get("dosi")
    assert result.get("sgg") == expected.get("sgg")

def test_restaurant_detail(client, access_db, create_dummy_restaurant, create_testuser_get_token):
    # 초기 유저정보 확인
    access_token = create_testuser_get_token
    
    # 레스토랑 상세정보?
    rest_pk = 1
    expected = Restaurant.objects.get(pk=rest_pk)
    assert expected
    
    # API로 가져온 상세정보와 기대값 비교하여 일치 확인
    serializer = FoodieDetailsSerializers(expected)
    expected_data = serializer.data
    url = f"/api/restaurant/{rest_pk}"
    response = client.get(url, 
                          headers={"Authorization": f"Bearer {access_token}"},content_type="application/json")
    
    assert response.status_code == 200
    assert response.data.get("id") == expected_data.get("id")
    assert response.data.get("name") == expected_data.get("name")
    assert response.data.get("name_address") == expected_data.get("name_address")
    assert response.data.get("sgg") == expected_data.get("sgg")
    assert response.data.get("sgg_code") == expected_data.get("sgg_code")
    assert response.data.get("start_date") == expected_data.get("start_date")