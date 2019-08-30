# -*- coding: utf-8 -*-

import time
from celery_app import app

@app.task
@app.task(queue='test_celey_queue_add')
def add(x, y):
    # time.sleep(0.01)
    return x + y

"""
注意, 我们给app.task这个装饰器传了queue这个参数, 这样当异步执行的时候,这个task会被丢到名称为test_celery_queue的队列中, 然后被为这个队列工作的worker拿到并执行。
当然， 我们也可以在CELERY_CONFIG中配置:
CELERY_ROUTES = {
     'celery_app.task1.add': 'test_celery_queue',
}
如果我们不指定queue的话，celery会默认自己指定一个队列。
task的队列一定要对应的worke， 否者就会只生产不消费， 这些task就永远不会被执行了。
"""