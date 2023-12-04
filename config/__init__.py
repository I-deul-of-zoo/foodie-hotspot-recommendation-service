from __future__ import absolute_import, unicode_literals
#absolute_import : celery.py 모듈 라이브러리들과 충돌하여 문제가 발생하지 않도록 도움
#

#이 구문은 shared_task를 위해 장고가 시작될 때 app이 항상 임포트 되도록 하는 역할을 합니다.
from .celery import app as celery_app

__all__ = ('celery_app', )