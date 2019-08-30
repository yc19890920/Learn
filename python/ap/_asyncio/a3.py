import asyncio
import uvloop
import aiomysql
from asyncio import Lock, Semaphore, BoundedSemaphore
lock = Lock()


async def hello():
    global num
    num = 1
    while num<=10:
        await asyncio.sleep(0.01)
        print('sleep done {}'.format(num))
        num += 1

if __name__ == "__main__":
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