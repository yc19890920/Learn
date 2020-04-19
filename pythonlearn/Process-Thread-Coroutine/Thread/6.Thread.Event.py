# -*- coding: utf-8 -*-

import threading
import time

class MyThread(threading.Thread):
    def __init__(self, signal):
        threading.Thread.__init__(self)
        self.singal = signal

    def run(self):
        print "I am %s,I will sleep ..."%self.name
        time.sleep(0.5)
         # 等待事件，进入等待阻塞状态
        self.singal.wait()
        # 收到事件后进入运行状态
        print "I am %s, I awake..." %self.name

if __name__ == "__main__":
    singal = threading.Event()
    for t in range(0, 3):
        thread = MyThread(singal)
        thread.start()

    time.sleep(3)
    # 发送事件通知
    print "main thread sleep 3 seconds... "
    singal.set()