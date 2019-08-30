from gevent.queue import Queue, Empty, LifoQueue, PriorityQueue
from functools import total_ordering

@total_ordering
class Job(object) :
    def __init__( self , prority , des ) :
        self.protity = prority
        self.des = des

    def __eq__(self, other):
        return self.protity == other.protity

    def __ne__(self, other):
        return not (self.protity == other.protity)

    def __lt__(self, other):
        return self.protity < other.protity

    def __str__(self):
        return "protity %d desc %s" %(self.protity, self.des)

def worker():
    q = PriorityQueue()
    q.put(Job(5,  'mid job'))
    q.put(Job(10, 'low job'))
    q.put(Job(1,  'high job'))

    while not q.empty():
        job = q.get()
        print(job)

if __name__ == "__main__":
    worker()