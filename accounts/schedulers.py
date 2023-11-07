from copy import deepcopy
import requests
import json

from django.db.models import Q
from django.contrib.auth import get_user_model

from foodiehotspots.models import Restaurant

User = get_user_model()

# WEBHOOK_URL = "https://discord.com/api/webhooks/1169806092138717267/57BBLDa6dr6GgE3p9U2humk-xHQmz1mJQNWUktYDIqUIsqmu5TH8ViQcF7HzcGaD-GQx"

WEBHOOK_URL = "https://discord.com/api/webhooks/1171271688420347925/7mHqAwmsk32ok27atslrNsWqL7ZUxnizyjoX-dPInavG-BRfaKMSHfzC01f-EfYkqh7h"


WEBHOOK_BODY = {
    "username": "점심추천 Bot",
    "avatar_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRN9lF93jsUSQ2J5jX4f4OcOvJf4I37mCdrfg&usqp=CAU",
    "content": "Your LunchHere! 오늘의 점심 추천 맛집은~",
    "embeds": []
}


class RestaurantStructure():
    def __init__(self, username, restaurant, color=37411):
        self.frame = {
            "description": f"{username}님 점심추천 드려요!",
            "color": 37411,
            "fields": [
                {
                    "name": restaurant.name,
                    "value": restaurant.food_category,
                },
                {
                    "name": "지번주소",
                    "value": restaurant.address_lotno
                },
                {
                    "name": "도로명주소",
                    "value": restaurant.address_roadnm
                }
            ],
            "footer": {
                "text": "언제나 당신을 위한 맛집과 함께 돌아올게요, Enjoy your LunchHere :)",
                "icon_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRN9lF93jsUSQ2J5jX4f4OcOvJf4I37mCdrfg&usqp=CAU"
            }
        }
    
    def get_object(self):
        return self.frame


## 위치 기반으로 음식점 리스트 가져오기
def get_lunch_list(user, radius=1.1):
    if user:
        print(user.username)
        # print("lat:", user.latitude)
        # print("lon:", user.longitude)
        api_url = "http://localhost:8000/api/restaurant/"
        parameter = {
                "lon": user.longitude,
                "lat": user.latitude,
                "radius": radius,
                # "sorting": None,
            }
        
        response = requests.get(api_url, params=parameter)
        if response.status_code == 200:
            json_obj = json.loads(response.text)
            result = json_obj['results'] # dict원소 list
            # print("request done:", result)
            
            if len(result) > 5:
                result = result[:5]
            
            restaurants = Restaurant.objects.filter(Q(id=result[0]['id']) | Q(id=result[1]['id']) | Q(id=result[2]['id']))
            menu_list = [RestaurantStructure(username=user.username, restaurant=r) for r in restaurants]
            return menu_list
        else:
            print("response fail. code:", response.status_code)


def send_lunch_notification(user, menu_list):
    headers = {
        "Content-Type":"application/json",
        "Cookie": "__cfruid=4204ca82a236d868f6c764aa062839306010699a-1699248683; __dcfduid=bd8c18f87c6511ee8b755e311c07e095; __sdcfduid=bd8c18f87c6511ee8b755e311c07e0954b57fa183bc003786cf133eb74b1b27210c5516f12386a006bac030e6694706b; _cfuvid=lPN6NFrR_ZglEs5bllqtEmqIyfyffIaH81_AR1_DQM4-1699248683966-0-604800000"}
    body = deepcopy(WEBHOOK_BODY)
    
    for m in menu_list:
        body["embeds"].append(m.get_object())
    
    print(body)
    response = requests.post(WEBHOOK_URL, headers=headers, json=body) ## webhook

    # if response.status_code == 200:
    #     print("success!!")
    # else:
    #     raise ValueError(f"잘못된 요청입니다~~. code: {response.status_code}")
   
    
def recommend_lunch():
    users = User.objects.filter(is_recommend=True)
    print("users:", users)
    for user in users:
        menu_list = []
        menu_list = get_lunch_list(user)
        send_lunch_notification(user, menu_list)
    