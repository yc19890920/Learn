# -*- coding: utf-8 -*-

import time
from celery_app import app

@app.task
@app.task(queue='test_celey_queue_multiply')
def multiply(x, y):
    # time.sleep(0.02)
    return x * y
