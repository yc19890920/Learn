# -*- coding: utf-8 -*-

from celery import Celery
from celery import platforms

platforms.C_FORCE_ROOT = True

# 第一个参数是实例的名称,  也可以使用模块的名字.
# broker参数是消息代理人url.
# 还有一个backend参数，当我们需要拿到异步任务的返回时需要用到.
# 这里就直接略过了.
app = Celery('demo')
app.config_from_object('celeryApp.celeryconfig')   # 通过 Celery 实例加载配置模块

# from conf import settings
# from lib import DBkit
#
# mysqlPool = DBkit.getDBObject(
#     creater='mysql',
#     dbtype='edm_web',
#     params=settings.DATABASES['mysql']['edm_web'],
#     charset='UTF8',
#     outerr=True
# )

