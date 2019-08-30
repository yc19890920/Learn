import gevent.monkey
gevent.monkey.patch_all()
import gevent
from gevent.pool import Pool

def hello():
    global num
    num = 1
    while num<=10000:
        # print(num)
        gevent.sleep(0.01)
        # await asyncio.sleep(random.random())
        # await asyncio.sleep(random.choice([0.1, 0.02, 0.03, 0.04, 0.05]))
        print('sleep done {}'.format(num))
        num += 1

import time
start = time.time()
tasks = []
coroutine_num = 10
for i in range(coroutine_num):
    tasks.append(gevent.spawn(hello))

gevent.joinall(tasks)
end = time.time()
print("Total Time: {}".format(end - start))