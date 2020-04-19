# -*- coding: utf-8 -*-

from time_decorator import timeout as timeout2
from threading_timeout_dec import timeout
from time import sleep, time
import threading

from multiprocessing.dummy import Pool as ThreadPool

@timeout(1)
def processNum(num):
    num_add = num + 1
    # results.append(str(threading.current_thread()) + ": " + str(num) + " → " + str(num_add))
    sleep(2)
    return str(threading.current_thread()) + ": " + str(num) + " → " + str(num_add)

def main():
    ts = time()
    pool = ThreadPool(4)
    results = pool.map(processNum, range(4))
    pool.close()
    pool.join()
    for _ in results:
        print _
    print("cost time is: {:.2f}s".format(time() - ts))


if __name__ == "__main__":
    main()