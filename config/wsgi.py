"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

## 여기서 실행하면 스케쥴러 함수가 한 주기에 한 번만 실행됨.
if settings.SCHEDULER_DEFAULT:
    from accounts import tasks
    tasks.start()