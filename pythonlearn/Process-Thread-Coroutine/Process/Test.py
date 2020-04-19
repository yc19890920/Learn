# -*- coding;utf-8 -*-

import time
import random
import itertools
import multiprocessing

MAX = 2**6
def producerLoop(q):
    c = itertools.count(start=1, step=1)
    while True:
        e = c.next()
        if e>MAX:  break
        q.put(e)
        time.sleep(0)
        # time.sleep(random.randint(1, 100)*random.choice([0.001, 0.005]))

def consumerLoop(q, name):
    while True:
        try:
            e = q.get(timeout=30)
            print '-----{}: {}------'.format(name, e)
            # time.sleep(random.randint(1, 100)*random.choice([0.001, 0.005]))
        except BaseException as e:
            print e
            break

def main():
    q = multiprocessing.Queue()
    processes = [  multiprocessing.Process( name='consumerLoop-1', target=producerLoop, args=(q, )) ]
    for x in range(10):
        name='consumerLoop-{}'.format(x)
        processes.append( multiprocessing.Process(
            name=name, target=consumerLoop, args=(q, name, )
        ))

    for P in processes:
        P.start()

    for P in processes:
        P.join()


if __name__ == "__main__":
    main()