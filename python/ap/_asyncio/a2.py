import asyncio
import uvloop
from asyncio import Lock, Semaphore, BoundedSemaphore

lock = Lock()
import random

async def hello():
    global num
    num = 1
    while num<=10000:
        # print(num)
        await asyncio.sleep(0.01)
        # await asyncio.sleep(random.random())
        # await asyncio.sleep(random.choice([0.1, 0.02, 0.03, 0.04, 0.05]))
        print('sleep done {}'.format(num))
        num += 1
        # with await lock:
        #     num += 1

import time
start = time.time()
coroutine_num = 10
tasks = []
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()
for i in range(coroutine_num):
    tasks.append(hello())
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
end = time.time()
print("Total Time: {}".format(end - start))

# import threading
# import asyncio
# num = 0
# @asyncio.coroutine
# def hello():
#     global num
#     while num<=30:
#         print(num)
#         yield from asyncio.sleep(0.2)
#         print('sleep done')
#         num += 1
#
# loop = asyncio.get_event_loop()
# tasks = [hello(), hello(),hello()]
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()