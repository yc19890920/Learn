# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

### ------增加gevent 设置------------ ###
# from gevent import monkey
# monkey.patch_all()
### ------------------ ###

import os
from celery import Celery, platforms

# 为celery程序设置DJANGO_SETTINGS_MODULE环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dblog.settings')

app = Celery('dblog')
platforms.C_FORCE_ROOT = True

# 从Django的设置文件中导入CELERY设置
app.config_from_object('django.conf:settings', namespace='CELERY')


######################################
#一次性添加多个配置
# 一下配置也可以在django settings设置
# app.conf.update(
#     CELERY_TASK_SERIALIZER='json',
#     CELERY_ACCEPT_CONTENT=['json'], # Ignore other content
#     CELERY_RESULT_SERIALIZER='json',
#     CELERY_TIMEZONE='Europe/Oslo',
#     CELERY_ENABLE_UTC=True,
# )

#处理繁重任务的专用队列
CELERY_ROUTES = {
    'app.blog.tasks.celery_send_email': 'high-priority:1',
}
#限制任务的速率，这样每分钟只允许处理 10 个该类型的任务
CELERY_ANNOTATIONS = {
    'tasks.add': {'rate_limit': '10/m'}
}
# CELERY_ANNOTATIONS={'*':{'rate_limit':'10/s'}} ,  #限制所有任务处理
# [并发设置]
CELERYD_CONCURRENCY = 20   #默认是你的cpu可用数量


######################################









# 从所有已注册的app中加载任务模块
app.autodiscover_tasks()


# celery 定时任务
from .celery_schedule import CELERYBEAT_SCHEDULE

app.conf.update(
    CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE
)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
