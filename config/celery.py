from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config',
        broker='amqp://',
        backend='rpc://',
        include=['user.tasks'])

app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.update(
    # task_routes = {
    #     'user.tasks.send_email': {'queue':'email'},
    #     'user.tasks.task_scrappy_naver': {'queue':'naver'},
    #     'user.tasks.task_scrappy_daum': {'queue':'daum'},

    # },
# )
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

app.conf.beat_schedule = {
    'add-every-minutes-naver':{
    'task':'user.tasks.task_scrappy_naver',
    'schedule':crontab(minute='*/15', hour='5-22')
    },
    'add-every-minutes-daum':{
    'task':'user.tasks.task_scrappy_daum',
    'schedule':crontab(minute='*/15', hour='5-22')
    }
}