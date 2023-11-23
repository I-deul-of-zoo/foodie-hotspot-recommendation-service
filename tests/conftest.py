import pytest
#로그인시 받는 토큰을 모든 test에 적용하기 위한 방법
#로그인 test는 따로 존재 합니다.
from accounts.models import User, Location
import json
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from typing import Iterable

import pytest

from django_redis import get_redis_connection

from django.core.cache import cache


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        connection = get_redis_connection("default")
        connection.flushdb()
        yield
        connection.flushdb()

@pytest.fixture
def user():
    return get_user_model().objects.create_user(
        username='testuser',
        password='testpassword'
    )

@pytest.fixture
def access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


@pytest.fixture()
def access_db(db):
    pass

@pytest.fixture()
def create_locations(access_db):
    from utils.location import location_load
    location_load.load_to_db()
    
    
@pytest.fixture()
def create_dummy_restaurant(access_db):
    import csv
    from foodiehotspots.models import Restaurant
    with open("./utils/restaurant_test_data.csv", "r", encoding="utf-8-sig") as f:
        csv_to_list = list(csv.DictReader(f))

        for i, row in enumerate(csv_to_list):
            row["name_address"] = row["name"] + row["address_roadnm"] + row["address_lotno"]
            Restaurant.objects.create(**row)