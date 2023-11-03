import time
from apscheduler.schedulers.background import BackgroundScheduler
from . import tasks


def schedule_process():
  scheduler = BackgroundScheduler()
  scheduler.add_job(tasks.my_scheduled_task, 'cron',  minute=1)
  scheduler.start()
