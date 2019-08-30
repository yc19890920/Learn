import os
from celery import Celery, platforms


# 为celery程序设置 DJANGO_SETTINGS_MODULE 环境变量
# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djusecelery.settings')


# 注册Celery的APP
app = Celery('djusecelery')
# 从Django的设置文件中导入CELERY设置
# 绑定配置文件
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现各个app下的tasks.py文件
# 从所有已注册的app中加载任务模块
app.autodiscover_tasks()
# platforms.C_FORCE_ROOT = True

# celery 定时任务
from .celery_schedule import CELERY_BEAT_SCHEDULE
app.conf.update(
    CELERY_BEAT_SCHEDULE=CELERY_BEAT_SCHEDULE,
    # CELERY_ANNOTATIONS = {
    #     # 限制每分钟完成10个任务
    #     'app.blog.tasks.task_number_one': {'rate_limit': '2/m'},
    #     'app.blog.tasks.task_number_three': {'rate_limit': '5/m'},
    # }
)


#

# from kombu import Exchange, Queue
# # default_exchange = Exchange('default', type='direct')
# # media_exchange = Exchange('media', type='direct')
#
# app.conf.task_queues = (
#     Queue('default', Exchange('default', type='direct'), routing_key='default'),
#     Queue('videos', Exchange('media', type='direct'), routing_key='media.video'),
#     Queue('images', Exchange('media', type='direct'), routing_key='media.image')
# )
# 下面的配置改变默认队列的名字:
app.conf.task_default_queue = 'default-celery'
# app.conf.task_default_exchange = 'default'
# app.conf.task_default_routing_key = 'default'

app.conf.task_routes = (
    [
        ('app.blog.tasks.task_number_one', {'queue': 'task_number_one'}),
        ('app.blog.tasks.task_number_two', {'queue': 'task_number_two'}),
        ('app.blog.tasks.task_number_three', {'queue': 'task_number_three'}),

        # ('feed.tasks.*', {'queue': 'feeds'}),
        # ('web.tasks.*', {'queue': 'web'}),
        # (re.compile(r'(video|image)\.tasks\..*'), {'queue': 'media'}),
    ],
)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))

#
# # ---------------------------------------------------------------------------------
# #一次性添加多个配置
# # 一下配置也可以在django settings设置
# app.conf.update(
#     CELERY_TASK_SERIALIZER='json',
#     CELERY_ACCEPT_CONTENT=['json'], # Ignore other content
#     CELERY_RESULT_SERIALIZER='json',
#     CELERY_TIMEZONE='Europe/Oslo',
#     CELERY_ENABLE_UTC=True,
# )
#
# #处理繁重任务的专用队列
# CELERY_ROUTES = {
#     'app.blog.tasks.celery_send_email': 'high-priority:1',
# }
# #限制任务的速率，这样每分钟只允许处理 10 个该类型的任务
# CELERY_ANNOTATIONS = {
#     'tasks.add': {'rate_limit': '10/m'}
# }
# # CELERY_ANNOTATIONS={'*':{'rate_limit':'10/s'}} ,  #限制所有任务处理
# # [并发设置]
# CELERYD_CONCURRENCY = 20   #默认是你的cpu可用数量
# # ---------------------------------------------------------------------------------