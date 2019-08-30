# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.schedules import crontab

# Broker and Backend
BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

# Timezone
CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'
CELERY_ENABLE_UTC=True

# CELERY_CONFIG = {
#     'CELERY_TIMEZONE': 'Asia/Shanghai',
#     'CELERY_ENABLE_UTC': True,
#
#     # content
#     'CELERY_TASK_SERIALIZER': 'json',
#     'CELERY_RESULT_SERIALIZER': 'json',
#     'CELERY_ACCEPT_CONTENT': ['json'],
#     'CELERYD_MAX_TASKS_PER_CHILD': 1,
# }


# import
CELERY_IMPORTS = (
    'celeryApp.tasks.task1',
    'celeryApp.tasks.task2',
    'celeryApp.tasks.task3',
)

# CELERY_ROUTES = {
#      'celeryApp.tasks.task1.add': 'test_celery_queue_task1_add',
#      'celeryApp.tasks.task2.add': 'test_celery_queue_task2_multiply',
#      'celeryApp.tasks.task3.add': 'test_celery_queue_task3_add',
# }

# schedules
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
        'task': 'celeryApp.tasks.task1.add',
        'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
        'args': (5, 8)                           # 任务函数参数
    },

    'multiply-at-some-time': {
        'task': 'celeryApp.tasks.task2.multiply',
        'schedule': crontab(hour=17, minute=30),   # 每天早上 9 点 50 分执行一次
        'args': (3, 7)                            # 任务函数参数
    }
}