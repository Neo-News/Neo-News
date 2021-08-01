from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule ={
#     'task-number-one': {
#         'task': 'user.tasks.task_scrappy_daum', # 실행함수
#         'schedule': crontab(minute='*/4', hour='*,5-22')
#     },
#     'task-number-two': {
#         'task': 'user.tasks.task_scrappy_naver', # 실행함수
#         'schedule': crontab(minute='*/3', hour='*,5-22')
#     },
# }


app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))