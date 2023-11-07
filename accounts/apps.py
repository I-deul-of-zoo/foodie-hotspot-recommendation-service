from django.apps import AppConfig
from django.conf import settings

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    ## 여기서 스케쥴러를 실행하면 왜 2번씩 실행될까
    # def ready(self): #앱 초기화 및 설정
    #     # super().ready()
        
    #     if settings.SCHEDULER_DEFAULT:
    #         if not getattr(AccountsConfig, 'scheduler_started', False):
    #             from accounts import tasks
    #             tasks.start()
            
    #         AccountsConfig.scheduler_started = True