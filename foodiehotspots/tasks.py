from __future__ import absolute_import, unicode_literals
from foodiehotspots.scheduler import RestaurantScheduler, DiscordWebHooksScheduler
from celery import shared_task


@shared_task()
def discord_scheduler_task():  #웹훅 스케줄러(점심추천)
    scheduler = DiscordWebHooksScheduler()
    scheduler.recommend_lunch()

@shared_task()
def restaurant_scheduler_task():  #식당 정보 스케줄러
    scheduler = RestaurantScheduler()
    scheduler.restaurant_scheduler()