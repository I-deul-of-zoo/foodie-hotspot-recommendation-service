from django.apps import AppConfig
from . import operator
import os
from config import settings

class FoodiehotspotsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'foodiehotspots'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) is not None:
            if settings.SCHEDULER_DEFAULT:
                operator.schedule_process()

    