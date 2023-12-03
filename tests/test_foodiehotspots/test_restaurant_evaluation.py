import pytest
from mixer.backend.django import mixer
from django.urls import reverse
from rest_framework import status

from foodiehotspots.models import Restaurant, Rate
from foodiehotspots.views import EvalCreateView
from foodiehotspots.serializers import EvalCreateSerializers

pytestmark = pytest.mark.django_db

def create_request_data(restaurant_id, score):
    return {
        'restaurant_id': restaurant_id,
        'score': score,
        'content': 'Test content'
    }

# 평균 평점을 계산하는 함수
def expected_average_score(new_score, current_average_score, total_rates):
    return (current_average_score * total_rates + new_score) / (total_rates + 1)

def test_eval_create_view(access_db, client, access_token, create_dummy_restaurant):
    
    # create_dummy_restaurant를 session으로 하려고 했으나 안됨 (원인 파악 못했습니다.)
    # 인자로 넣으면 여러번 들어가서 최근에 넣은 last만 가지고 오도록 함.
    # 왜 다른 index는 못가지고 오는 것인지 모르겠습니다.
    # ex) id = 10을 주면 가지고 올 수 없더라구요
    assert Restaurant.objects.exists()
    
    restaurant = Restaurant.objects.last()
    request_data = create_request_data(restaurant.id, 4)
    restaurant_pk = restaurant.id

    # 예상 평균 계산
    expected_avg = expected_average_score(request_data['score'], restaurant.average_score, restaurant.rates.count() + 1)

    url = f"/api/restaurant/{restaurant_pk}/evaluation"

    response = client.post(
        url, 
        headers={"Authorization": f"Bearer {access_token}"},
        data=request_data,
        content_type="application/json"
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    assert 'avg_score' in response.data
    assert 'eval_ids' in response.data

    object_eval_ids = list(response.data['eval_ids'].values('content', 'score'))[0]

    assert object_eval_ids['content'] == "Test content"
    assert object_eval_ids['score'] == 4.0

    # 레스토랑 평균 평점 업데이트 확인
    updated_restaurant = Restaurant.objects.get(id=restaurant_pk)
    assert updated_restaurant.average_score == expected_avg