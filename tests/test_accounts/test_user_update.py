import json
import pytest

from django.core.cache import cache


@pytest.mark.django_db
def test_user_check(client, access_token):

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

def test_user_update(client, access_token, access_db):  
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
    