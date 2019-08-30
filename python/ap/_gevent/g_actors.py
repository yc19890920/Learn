# -*- coding: utf-8 -*-
from gevent.queue import Queue
from gevent import Greenlet
from message import observable

class Actor(Greenlet):
    def __init__(self):
        self.inbox = Queue()
        Greenlet.__init__(self)

    def send(self, message):
        self.inbox.put(message)

    def receive(self, message):
        raise NotImplemented()

    def _run(self):
        self.running = True

        while self.running:
            message = self.inbox.get()
            self.receive(message)


@observable
class Publisher(Actor):
    def __init__(self, subject):
        self.subject = subject
        Actor.__init__(self)

    def subcribe(self, observer):
        self.sub(self.subject, observer.send)

    def publish(self, message):
        self.pub(self.subject, message)


import gevent


class Pinger(Publisher):
    def receive(self, message):
        print(message)
        self.publish('ping')
        gevent.sleep(1)


class Ponger(Publisher):
    def receive(self, message):
        print(message)
        self.publish('pong')
        gevent.sleep(1)


ping = Pinger('evt.ping')
pong = Ponger('evt.pong')

ping.subcribe(pong)
pong.subcribe(ping)
ping.start()
pong.start()

ping.publish('start')
gevent.joinall([ping, pong])

