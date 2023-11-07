import os

from django.apps import AppConfig
from django.conf import settings

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self): #앱 초기화 및 설정
        ## runserver 시 코드 읽을 때 한번, 로드할 때 한번 동작해서 task가 스케쥴러에 두번 설정되므로 RUN_MAIN 일때만 동작하도록 하는 코드.
        if os.environ.get('RUN_MAIN', None) is not None:
            # if settings.SCHEDULER_DEFAULT:
            #     operator.schedule_process()
            if settings.SCHEDULER_DEFAULT:
                from foodiehotspots import tasks
                tasks.start()
                