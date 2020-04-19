# -*- coding: utf-8 -*-

import multiprocessing
import time

###################################################
# 1.单个进程

def worker(interval):
    n = 5
    while n > 0:
        print("The time is {0}".format(time.ctime()))
        time.sleep(interval)
        n -= 1

# if __name__ == "__main__":
#     p = multiprocessing.Process(target=worker, args=(3,))
#     p.start()
#     print "p.pid:", p.pid
#     print "p.name:", p.name
#     print "p.is_alive:", p.is_alive()

###################################################
# 2.多个进程

def worker_1(interval):
    print "worker_1"
    time.sleep(interval)
    print "end worker_1"

def worker_2(interval):
    print "worker_2"
    time.sleep(interval)
    print "end worker_2"

def worker_3(interval):
    print "worker_3"
    time.sleep(interval)
    print "end worker_3"

if __name__ == "__main__":
    process = [
        multiprocessing.Process(target = worker_1, args = (2,)),
        multiprocessing.Process(target = worker_2, args = (3,)),
        multiprocessing.Process(target = worker_3, args = (4,))
    ]
    # 启动所有进程
    for P in process:
        P.start()

    print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print("child   p.name:" + p.name + "\tp.id" + str(p.pid))

    # # 主进程中等待所有子进程退出
    for P in process:
        P.join()


    # print("The number of CPU is:" + str(multiprocessing.cpu_count()))
    # for p in multiprocessing.active_children():
    #     print("child   p.name:" + p.name + "\tp.id" + str(p.pid))
    # print "END!!!!!!!!!!!!!!!!!"


###################################################
# 3. 进程定义为类

class ClockProcess(multiprocessing.Process):
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval

    def run(self):
        n = 5
        while n > 0:
            print("the time is {0}".format(time.ctime()))
            time.sleep(self.interval)
            n -= 1

# if __name__ == '__main__':
#     p = ClockProcess(3)
#     # 注：进程p调用start()时，自动调用run()
#     p.start()


###################################################
# 4. 加daemon属性
def worker(interval):
    print("work start:{0}".format(time.ctime()));
    time.sleep(interval)
    print("work end:{0}".format(time.ctime()));

# if __name__ == "__main__":
#     p = multiprocessing.Process(target = worker, args = (3,))
#     p.daemon = True
#     p.start()
#     print "end!"