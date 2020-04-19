# -*- coding: utf-8 -*-

import time
import threading
from twisted.internet import reactor

import logging
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))

log = logging.getLogger('test')
log.addHandler(_handler)
log.setLevel(logging.DEBUG)

gpd   = {                   # 全局公共数据 (Global Public Data)
    'task'    : None,       # 发送任务信息
    'speed'   : None,       # 当前任务发送速度
    'listname': None,       # 收件人地址列表名称
    'mailtpl' : None,       # 邮件模板对象
    'callback': None,       # 邮件发送完成后的回调函数
    'flagstop': None        # 程序中止标记位
}

stat_lock = threading.Lock()

stat = {
    'success': 0,
    'failure': 0
}

# 发送速度同步器 (每 10 秒同步一次)
def speedSynchronizer(user_id) :
    while True :
        if gpd['flagstop'] :  reactor.stop()
        gpd['speed'] = 5
        log.info('synchronizer speed (%d)' % gpd['speed'])
        time.sleep(10)
        # time.sleep(0.01)
    return

# 统计处理器 (每 30 秒保存一次)
def statHandler(task_id) :
    while True :
        if gpd['flagstop'] : reactor.stop()
        saveSendStat(task_id, wait=False)
        time.sleep(30)
        # time.sleep(0.01)
    return

# 保存统计数据
def saveSendStat(task_id, wait=False) :
    log.info('saveSendStat after 30s...')
    if stat['success'] == 0 and stat['failure'] == 0 : return
    return


# 设置程序结束信号量
def set_signal(handler) :
    import signal
    signal.signal(signal.SIGINT,  handler)      # 处理 Ctrl-C
    signal.signal(signal.SIGTERM, handler)      # 处理 kill
    signal.signal(signal.SIGALRM, handler)      # 处理 signal.alarm()

import traceback
def stack():
    print 'The python stack:'
    traceback.print_stack()

############################################################

# 信号量回调操作
# noinspection PyUnusedLocal
def sigcb(signum, frame) :
    gpd['flagstop'] = True

if __name__ == "__main__":
    EXIT_CODE = 0
    log.info('program start')
    set_signal(sigcb)
    try:
        reactor.callWhenRunning(stack)
        # 创建独立线程
        reactor.callInThread(speedSynchronizer, 2369)      # 发送速度同步器
        reactor.callInThread(statHandler, 123456)          # 发送统计处理器
        reactor.run(False)
    except BaseException as e:
        # dosomething
        EXIT_CODE = 1
    log.info('program quit')
    exit(EXIT_CODE)
