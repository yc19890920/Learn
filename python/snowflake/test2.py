# -*- coding:utf-8 -*-

import gevent
# 导入pysnowflake客户端
import snowflake.client as cli

# 链接服务端并初始化一个pysnowflake客户端
host = '192.168.1.24'
port = 30001
cli.setup(host, port)

signal_stop = False
fp = open("1.txt", 'a+')

def work1():
     while 1:
         if signal_stop: break
         # 生成一个全局唯一的ID（在MySQL中可以用BIGINT UNSIGNED对应）
         guid = cli.get_guid()
         print guid

         # 查看当前状态
         stats = cli.get_stats()
         print stats
         fp.write("{}\r\n".format(guid))

######################################################
# --------------信号量处理---------------
def initGeventSignal(handler):
    import signal
    gevent.signal(signal.SIGINT, handler, 'sigint')  # 处理 Ctrl-C
    gevent.signal(signal.SIGTERM, handler, 'sigterm')  # 处理 kill
    gevent.signal(signal.SIGALRM, handler, 'sigalrm')  # 处理 signal.alarm()

# 信号量处理
def signalHandle(mode):
    global signal_stop
    signal_stop = True

def main():
    initGeventSignal(signalHandle)
    allspawn = [gevent.spawn(work1) for _ in xrange(10)]
    gevent.joinall(allspawn)

if __name__ == '__main__':
    print("program start...")
    main()
    fp.close()
    print("program end...")



