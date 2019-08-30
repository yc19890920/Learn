import gevent.monkey
gevent.monkey.patch_all()
from pykka.gevent import GeventActor as Actor
from pykka import ActorRegistry

class Adder(Actor):

    def add_one(self, i):
        print('{} is increasing {}'.format(self, i))
        gevent.sleep(0)
        return i + 1

class Bookkeeper(Actor):

    def __init__(self, remoter):
        super(Bookkeeper, self).__init__()
        self.remoter = remoter

    def count_to(self, target):
        i = 0
        while i < target:
            i = self.remoter.add_one(i).get()
            print('{} got {} back'.format(self, i))

adder = Adder.start().proxy()
bookkeeper = Bookkeeper.start(adder).proxy()
bookkeeper.count_to(10).get()
ActorRegistry.stop_all()