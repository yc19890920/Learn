# -*- coding: utf-8 -*-

import random
from celery_app import task1
from celery_app import task2

for i in range(10):
    # task1.add.apply_async(args=[1, 2])        # 也可用 task1.add.delay(2, 8)
    # task2.multiply.apply_async([2, 3])   # 也可用 task2.multiply.delay(3, 7)
    #
    task1.add.apply_async(args=[random.randint(1,100),random.randint(1,100)])        # 也可用 task1.add.delay(2, 8)
    task2.multiply.apply_async(args=[random.randint(1,100),random.randint(1,100)])   # 也可用 task2.multiply.delay(3, 7)

# print 'hello world'
