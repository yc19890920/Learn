import asyncio
import random
import time

from concurrent.futures import ThreadPoolExecutor
_executor = ThreadPoolExecutor(15)

_loop = asyncio.get_event_loop()


def _get_cloud_ip(index):
    time.sleep(random.randint(1,10))
    print("=====================index:{}".format(index))
    return [index]


async def generate_cloud_ip(index):
    cloud_ips = await _loop.run_in_executor(_executor, _get_cloud_ip, index, )
    if not cloud_ips:
        return None
    return cloud_ips

tasks = []
for index in range(10):
    tasks.append(asyncio.ensure_future(generate_cloud_ip(index)))

_loop.run_until_complete(asyncio.gather(*tasks))

x = []
for task in tasks:
    cloud_ips = task.result()
    if cloud_ips and isinstance(cloud_ips, list):
        x += cloud_ips
    else:
        print(cloud_ips)

print(x)

_loop.close()



