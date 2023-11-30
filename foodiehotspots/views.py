import math
import jwt

from config import settings
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication

from foodiehotspots.models import Restaurant, Rate
from foodiehotspots.serializers import RestaurantSerializer, FoodieDetailsSerializers, EvalCreateSerializers

logger = settings.CUSTOM_LOGGER

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'


class RestaurantList(ListAPIView):
    '''
    GET /api/restaurant/?lat=37.4&lon=127.08
    GET /api/restaurant/?lat=37.4&lon=127.08&radius=3.0&sorting=average_score
    '''
    permissions_classes = [AllowAny]

    serializer_class = RestaurantSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        radius = self.request.query_params.get('radius', 1.1)
        sorting = self.request.query_params.get('sorting', 'distance')  # 'distance' or 'score'

        user_point = (float(lat), float(lon))

        # 주어진 범위 안에 있는 식당 리스트
        within_radius = []
        all_restaurants = Restaurant.objects.all()

        for r in all_restaurants:
            restaurant_point = (float(r.longitude), float(r.latitude))
            distance = lat_lon_to_km(user_point, restaurant_point)
            if distance <= float(radius):
                within_radius.append((distance, r))

        sorted_restaurants = []

        try:
            for i in range(len(within_radius)):
                distance, r = within_radius[i]
                sorted_restaurants.append({"distance": distance, "restaurant_id": r.id})
        except IndexError:
            raise ValueError(detail="인덱스가 범위를 벗어났습니다.")

        # 거리 순 정렬
        if sorting == 'distance':
            within_radius.sort(key=lambda x: x[0])
            sorted_restaurant = [r[1] for r in within_radius]  # sorted_distance_restaurant
        
        # average_score 내림차순 정렬
        elif sorting == 'average_score':
            within_radius.sort(key=lambda x: x[1].average_score, reverse=True)
            sorted_restaurant = [r[1] for r in within_radius]  # sorted_averageScore_restaurant
        else:
            raise ParseError()
        
        return sorted_restaurant

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def lat_lon_to_km(point_1, point_2):
    lat1 = point_1[1]
    lon1 = point_1[0]
    lat2 = point_2[1]
    lon2 = point_2[0]

    # R = 6371  # km
    R = 1  # km
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c


class FoodieDetailsView(RetrieveModelMixin, GenericAPIView):
    serializer_class = FoodieDetailsSerializers
    # JWT 인증방식 클래스 지정하기
    authentication_classes = [JWTAuthentication]

    queryset = Restaurant.objects.all()
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        return obj
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        '''
        (issue #19) 1단계
        - 600초 동안 호출되는 모든 데이터 다 캐싱
        '''
        cache_key = f'foodie_detail_{kwargs["pk"]}'  # 캐시 키 생성

        # 캐시에서 데이터 가져오기
        cached_data = cache.get(cache_key)

        if cached_data is not None:
            # 캐시에 데이터가 있을 경우, 캐싱된 데이터 반환
            return Response(cached_data, status=status.HTTP_200_OK)

        # 캐시에 데이터가 없는 경우 DB에서 데이터 조회
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        '''
        (issue #19) 2단계
        - 1단계를 만족하면서, 5개 이상의 평가가 존재하고 평점은 4.0 이상인 데이터만 600초 동안 캐싱
        '''
        # print(obj.score)
        # print(type(obj.score))  # float
        # print(obj.rates.count())
        if obj.rates.count() >= 5 and obj.average_score >= 4.0 :
            cache.set(cache_key, serializer.data, 600)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

class EvalCreateView(CreateModelMixin, GenericAPIView):
    authentication_classes = [JWTAuthentication]  # 인증
    permission_classes = [IsAuthenticated]  # 권한(인가)
    serializer_class = EvalCreateSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 평가 데이터를 저장
        self.perform_create(serializer)

        # 평가가 생성되면 해당 맛집의 평점을 업데이트
        restaurant_id = self.kwargs.get('pk')
        restaurant_object = get_object_or_404(Restaurant, id=restaurant_id)
        rate_score = int(request.data.get('score'))

        # 현재까지의 총 평점과 평가 횟수 가져오기
        total_rate_count = restaurant_object.rates.count()
        total_score = restaurant_object.average_score * total_rate_count
        
        # 새로운 평가 반영하여 평균 계산
        new_total_score = total_score + rate_score
        new_average_score = new_total_score / (total_rate_count + 1)
        
        # 맛집의 평균점수 업데이트
        restaurant_object.average_score = new_average_score
        restaurant_object.save()

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )

    def get_object(self, request):
        token_str = request.headers.get("Authorization").split(' ')[1]
        data = jwt.decode(token_str, SECRET_KEY, ALGORITHM)
        obj = get_object_or_404(Rate, user=data['user_id'])
        return obj
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)