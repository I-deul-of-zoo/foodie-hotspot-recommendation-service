import json
import pytest
from django.core.cache import cache
from accounts.models import Location
BASE_URL = '/api/'


class TestLocationList:
    pytestmark = pytest.mark.django_db        
    #특정 지역 데이터 확인
    def test_spec_location_list(self, client, access_token, create_locations, django_db_setup):
        
        url = f"{BASE_URL}account/locations/"
        response = client.get(
            url,
            headers={"Authorization": f"Bearer {access_token}"},
            content_type="application/json",
        )
        
        assert response.status_code == 200
        #또한 cache에 데이터가 잘올라갔는지 확인
        cached_data = cache.get('locations')
        assert cached_data is not None
        assert len(cached_data) == response.data.get("count")
        
        url = f"{BASE_URL}account/locations/"
        expected = {"dosi": "강원", "sgg": "강릉시"}
        response = client.get(
            url,
            expected,
            headers={"Authorization": f"Bearer {access_token}"},
            content_type="application/json",
        )
        
        assert response.status_code == 200
        assert response.data.get("count") == 1
        assert expected["dosi"] == response.data.get("results")[0]["dosi"]
        assert expected["sgg"] == response.data.get("results")[0]["sgg"]
        
        cached_response = client.get(
            url,
            expected,
            headers={"Authorization": f"Bearer {access_token}"},
            content_type="application/json",
        )
        
        assert response.data == cached_response.data
        
    
        
        