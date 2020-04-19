# -*- coding: utf-8 -*-

import multiprocessing

def writer_proc(q):
    try:
        # q.put(1, block = False)
        q.put(1)
    except:
        pass

def reader_proc(q):
    try:
        # x = q.get(block = False)
        x = q.get()
        print x
    except:
        pass

if __name__ == "__main__":
    q = multiprocessing.Queue()
    writer = multiprocessing.Process(target=writer_proc, args=(q,))
    writer.start()

    reader = multiprocessing.Process(target=reader_proc, args=(q,))
    reader.start()

    reader.join()
    writer.join()