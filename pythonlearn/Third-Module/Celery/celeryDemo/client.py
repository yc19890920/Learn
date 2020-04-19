# -*- coding: utf-8 -*-

import random
from celeryApp.tasks import task1, task2, task3

for i in range(10):
    task3.add.apply_async(args=[random.randint(1,100),random.randint(1,100)])        # 也可用 task1.add.delay(2, 8)
    # task2.multiply.apply_async(args=[random.randint(1,100),random.randint(1,100)])   # 也可用 task2.multiply.delay(3, 7)

