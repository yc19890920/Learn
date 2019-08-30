# -*- coding: utf-8 -*-

import time
from celeryApp import app

# @app.task
@app.task(queue='celey_app:2017_08_22:task2.multiply')
def multiply(x, y):
    time.sleep(0.02)
    return x * y