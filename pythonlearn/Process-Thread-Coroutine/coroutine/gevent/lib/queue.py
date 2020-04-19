#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gevent.event
import heapq
import time


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