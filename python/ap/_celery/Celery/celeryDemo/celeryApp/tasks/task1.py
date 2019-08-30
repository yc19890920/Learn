# -*- coding: utf-8 -*-

import time
from celeryApp import app

from ..conf import settings
from ..lib import DBkit

mysqlPool = DBkit.getDBObject(
    creater='mysql',
    dbtype='edm_web',
    params=settings.DATABASES['mysql']['edm_web'],
    charset='UTF8',
    outerr=True
)

@app.task
# @app.task(queue='celey_app:2017_08_22:task1.add')
def add(x, y):
    time.sleep(0.01)
    sql = 'UPDATE core_customer SET company=%s WHERE  customer_id=2369;'
    args = ('TEST（测试）',)
    res = mysqlPool.do(sql, args)
    # print dir(app)
    # print dir(app.log)
    print '------------------: {}'.format(res)
    print '------------------{} + {} = {}'.format(x, y, x+y)
    # return x + y

"""
注意, 我们给app.task这个装饰器传了queue这个参数, 这样当异步执行的时候,这个task会被丢到名称为test_celery_queue的队列中, 然后被为这个队列工作的worker拿到并执行。
当然， 我们也可以在CELERY_CONFIG中配置:
CELERY_ROUTES = {
     'celery_app.task1.add': 'test_celery_queue',
}
如果我们不指定queue的话，celery会默认自己指定一个队列。
task的队列一定要对应的worke， 否者就会只生产不消费， 这些task就永远不会被执行了。
"""