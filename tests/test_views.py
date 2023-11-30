import pytest
from mixer.backend.django import mixer
from django.urls import reverse
from rest_framework import status
from tests.conftest import create_restaurant, user
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

def test_eval_create_view(user, create_restaurant, client, access_token):
    user = user
    restaurant = create_restaurant

    request_data = create_request_data(restaurant.id, 4)
    restaurant_pk = restaurant.id

    # 예상 평균 계산
    expected_avg = expected_average_score(request_data['score'], restaurant.average_score, restaurant.rates.count() + 1)

    url = f"/api/restaurant/{restaurant_pk}/evaluation"

    response = client.post(
        url, 
        headers={"Authorization": f"Bearer {access_token}"},
        data={
            "restaurant_id": request_data['restaurant_id'],
            "score": request_data['score'],
            "content": request_data['content'],
        },
        content_type="application/json"
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert 'avg_score' in response.data
    assert 'eval_ids' in response.data

    object_eval_ids = list(response.data['eval_ids'].values('content', 'score'))[0]

    assert object_eval_ids['content'] == "Test content"
    assert object_eval_ids['score'] == 4.0

    # [TODO] Serializer를 통해서 응답 데이터 비교
    # serializer_data = EvalCreateSerializers(response.data).data
    # assert serializer_data == response.data

    # 레스토랑 평균 평점 업데이트 확인
    updated_restaurant = Restaurant.objects.get(id=restaurant_pk)
    assert updated_restaurant.average_score == expected_avg