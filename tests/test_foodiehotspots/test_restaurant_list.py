import json
import pytest

from django.core.cache import cache

from foodiehotspots.models import Restaurant

BASE_URL = '/api/'

class TestRestaurantList:
    pytestmark = pytest.mark.django_db 
    #특정 지역 데이터 확인
    def test_restaurant_list(self, client, access_token):
      
        loc = {"lat": 37.33560775777259, "lon":127.09269462688626}
        url = f'{BASE_URL}restaurant/'
        response = client.get(url,
                              loc,
                            headers={"Authorization": f"Bearer {access_token}"},
                            content_type="application/json")
        assert response.data is not None
        
    

        