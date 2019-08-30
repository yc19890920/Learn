import time
import heapq
import uuid
import random
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import gevent.event
import gevent.backdoor
from gevent.queue import Queue, Empty, LifoQueue, PriorityQueue

class RetryQueue(object):
    def __init__(self):
        self._heap = []
        self._event = gevent.event.Event()

    def put(self, next_time, d):
        heapq.heappush(self._heap, (next_time, d))
        self._event.set()

    def get(self):
        while True:
            self._event.clear()
            if len(self._heap) > 0:
                next_time, d = self._heap[0]
                t = time.time()
                if t >= next_time:
                    _, dd = heapq.heappop(self._heap)
                    assert d is dd
                    return d
                else:
                    self._event.wait(next_time - t)
            else:
                self._event.wait()

def retry_put_routine():
    index = 1
    while True:
        ident = "{}--{}".format(str(uuid.uuid1()), index)
        retry.put( time.time() + random.randint(1, 30), ident )
        print('-----------put:', ident)
        index += 1
        if index == 10000:
            gevent.sleep(600)
        gevent.sleep(0.5)

def retry_routine():
    while True:
        d = retry.get()
        print('---------------------------------get:', d)
        # gevent.sleep(2)

def main():
    global retry
    retry = RetryQueue()
    all_routine = [
        # gevent.spawn(gevent.backdoor.BackdoorServer(('localhost', 6565)).serve_forever),
        gevent.spawn(retry_put_routine),
        gevent.spawn(retry_routine)
    ]
    gevent.joinall(all_routine)

if __name__ == "__main__":
    main()