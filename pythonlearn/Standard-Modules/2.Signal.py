#coding=utf8

import signal,os,time
def onsignal_term(a,b):
    print '收到SIGTERM信号'

def onsignal_quit(a,b):
    print '收到SIGQUIT信号'

def onsignal_alrm(a,b):
    print '收到SIGALRM信号'

signal.signal(signal.SIGTERM,onsignal_term)
signal.signal(signal.SIGQUIT,onsignal_quit)
signal.signal(signal.SIGALRM,onsignal_alrm)
signal.alarm(10)
while 1:
    print '进程id：',os.getpid()
    time.sleep(2)