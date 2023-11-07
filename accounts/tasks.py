from functools import partial
import time

from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django.db import models

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler

from accounts.schedulers import recommend_lunch


scheduler = None #스케줄러 전역 변수로 설정
    
def start():
    print('here!')
    scheduler = BackgroundScheduler()
    # DjangoJobStore : django 데이터베이스를 사용하여 스케쥴링 작업 저장 및 관리
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)
    
    # 이전 스케줄이 완료될 때까지 대기할 시간(초) 설정
    # scheduler.add_job(
    #     lunch_notification,
    #     trigger=CronTrigger(
    #         hour="11", minute="30"), # 실행 시간입니다. 매일 11시 30분에 실행합니다.
    #     id="my_job_b",
    #     max_instances=1,
    #     replace_existing=True ) 
    
    scheduler.add_job(
        partial(recommend_lunch),
        trigger=IntervalTrigger(
            seconds=10), # 10초에 한번씩
        id="recommend_lunch",
        max_instances=1,
        replace_existing=True,
        misfire_grace_time=1000) 
    # scheduler.add_job(job1, 'cron',minutes='0',misfire_grace_time=wait_time) #!매분 실행으로 테스트
    scheduler.start()
