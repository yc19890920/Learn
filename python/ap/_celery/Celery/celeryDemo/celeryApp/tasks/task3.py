# -*- coding: utf-8 -*-

import time
from celeryApp import app


# @app.task
@app.task(queue='celey_app:2017_08_22:task3.add')
# @app.task(queue='celey_app:2017_08_22:task1.add')
def add(x, y):
    time.sleep(0.01)
    print '--------------------', x, y
    return x + y