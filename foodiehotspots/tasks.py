import time
from functools import partial

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

from django.db import models
# from foodiehotspots.views import RestaurantScheduler
from foodiehotspots.scheduler import RestaurantScheduler, DiscordWebHooksScheduler


scheduler1 = None
scheduler2 = None

def start():
    scheduler1 = BackgroundScheduler(timezone='Asia/Seoul')  # 시간대 설정
    # DjangoJobStore : django 데이터베이스를 사용하여 스케쥴링 작업 저장 및 관리
    scheduler1.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler1)
    # 이전 스케줄이 완료될 때까지 대기할 시간(초) 설정
    wait_time = 1000
    job1 = partial(RestaurantScheduler.restaurant_scheduler, RestaurantScheduler())
    
    scheduler1.add_job(job1, 'cron', hour=2, misfire_grace_time=wait_time)  # 2시 실행(default)
    
    # scheduler1.add_job(job1, 'cron', minute='*',misfire_grace_time=wait_time) #!매분 실행으로 테스트
    scheduler1.start()

    
def schedule_process():
    scheduler2 = BackgroundScheduler()
    job2 = partial(DiscordWebHooksScheduler.recommend_lunch, DiscordWebHooksScheduler())
    #점심시간 30분전 식당 추천
    scheduler2.add_job(job2, 'cron', hour=10, minute=55)
    scheduler2.start()