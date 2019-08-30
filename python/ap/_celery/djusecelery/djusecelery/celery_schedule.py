# 定时任务
# The following lines may contains pseudo-code
from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    # 'task-number-one': {
    #     'task': 'app.blog.tasks.task_number_one',
    #     'schedule': crontab(minute=59, hour=23),
    #     'args': ( )
    # },
    # 'task-number-two': {
    #     'task': 'app.blog.tasks.task_number_two',
    #     'schedule': crontab(minute=0, hour='*/3,10-19'),
    #     'args': ( )
    # },
    #
    'hello-django-celery': {
        'task': 'app.blog.tasks.task_number_one',
        # 'schedule': timedelta(minutes=15),
        # 'schedule': timedelta(microseconds=100000),
        # 'schedule': timedelta(microseconds=1000),
        'schedule': timedelta(seconds=5),
        # 'schedule': timedelta(hours=15),
        'args': ( )
    },

    'task_number_three': {
        'task': 'app.blog.tasks.task_number_three',
        # 'schedule': timedelta(minutes=15),
        # 'schedule': timedelta(microseconds=100000),
        # 'schedule': timedelta(microseconds=1000),
        'schedule': timedelta(seconds=10),
        # 'schedule': timedelta(seconds=15),
        # 'schedule': timedelta(hours=15),
        'args': ( )
    },


    'excute_django_model': {
        'task': 'app.blog.tasks.excute_django_model',
        # 'schedule': timedelta(minutes=15),
        # 'schedule': timedelta(microseconds=100000),
        # 'schedule': timedelta(microseconds=1000),
        'schedule': timedelta(seconds=7),
        # 'schedule': timedelta(seconds=15),
        # 'schedule': timedelta(hours=15),
        'args': ( )
    },

    'excute_django_connection': {
        'task': 'app.blog.tasks.excute_django_connection',
        # 'schedule': timedelta(minutes=15),
        # 'schedule': timedelta(microseconds=100000),
        # 'schedule': timedelta(microseconds=1000),
        'schedule': timedelta(seconds=7),
        # 'schedule': timedelta(seconds=15),
        # 'schedule': timedelta(hours=15),
        'args': ( )
    },
}