# -*- coding: utf-8 -*-
#
import os
import sys
import time
import traceback
import threading
import logging
import logging.handlers

from lib import pyetc, pidfile, file_utils, magic_method
from db import MongoPool, MysqlPool

import redis
redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis = redis.StrictRedis(connection_pool=redis_pool)

ROOT = os.path.realpath(os.path.join(os.path.split(__file__)[0]))
# 全局变量
log = None
signal_stop = False
mysql_pool = None
mongo_cn = None
lock = threading.Lock()

############################################################
# 修改状态
def do_task(task, status):
    sql = "UPDATE ml_import SET status='%d' WHERE id='%d'" % (int(status), task['import_id'])
    res = mysql_pool.update(sql)
    return res

@magic_method.sync_lock(lock)
def get_task():
    sql = "SELECT id, customer_id, maillist_id, filepath, is_disorder FROM ml_import WHERE status='-1' AND is_newimport=1 ORDER BY id LIMIT 1"
    res = mysql_pool.getAll(sql)
    if not res:
        return 1, {}
    task = {
        'import_id' : int(res[0][0]),
        'user_id' : int(res[0][1]),
        'list_id' : int(res[0][2]),
        'path' : str(res[0][3]),
        'is_disorder': int(res[0][4]),
    }
    log.info(u'{}----------{}'.format(threading.currentThread().getName(), task))
    try:
        do_task(task, '0')
        return 2, task
    except:
        log.error(task + "\n" + traceback.format_exc())
        return 3, task

def startTask():
    null = 1
    while True:
        if null % 10000 == 0:
            null = 1
            log.info(u"{}, No task...".format(threading.currentThread().getName()))
            time.sleep(10)

        if signal_stop: break

        status, task = get_task()
        if status == 1:
            time.sleep(0.5)
            null += 1
            continue

        if status == 3:
            do_task(task, '-1')
            continue

        time.sleep(0.01)

def main():
    log.info("开始启动...")
    for doTaskThread in doTaskThreads:
        doTaskThread.setDaemon(True)
        doTaskThread.start()
    # doTaskThread.setDaemon(True)
    # doTaskThread.start()
    log.info("启动成功!")
    magic_method.emptyLoop()

############################################################
# 日志设置
def set_logger(log_file, is_screen=True):
    global log
    log = logging.getLogger('mail_import')
    log.setLevel(logging.INFO)
    format = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')

    log_handler = logging.handlers.RotatingFileHandler(log_file, 'a', 5000000, 4)
    log_handler.setFormatter(format)
    log.addHandler(log_handler)

    if is_screen:
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(format)
        log.addHandler(log_handler)
    else:
        f = open(log_file, 'a')
        sys.stdout = f
        sys.stderr = f

# 信号量处理
def signal_handle(mode):
    log.info(u"Catch signal: %s" % mode)
    global signal_stop
    signal_stop = True

# 初始化
def init():
    global mysql_pool, mongo_cn
    conf = pyetc.load(os.path.join(ROOT, 'conf', 'setting.conf'))

    # 获取数据库
    dbconf = {'mysql': conf.mysql, 'mongo': conf.mongo}

    try:
        mysql_pool = MysqlPool.Mysql(dbconf, log)
    except BaseException as e:
        log.error(u'init mysql pool exception.')
        log.error(traceback.format_exc())
        sys.exit(1)

    try:
        mongo_cn = MongoPool.Mongo(dbconf, log)
        mongo_cn.init()
    except BaseException as e:
        log.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    log_dir = os.path.join(ROOT, 'log')
    pid_dir = os.path.join(ROOT, 'pid')
    file_utils.make_dir([log_dir, pid_dir])
    log_file = os.path.join(log_dir, 'test.log')
    set_logger(log_file)

    pid_file = os.path.join(ROOT, 'pid', 'test.pid')
    pidfile.register_pidfile(pid_file)

    init()

    doTaskThreads = []
    for i in xrange(10):
        doTaskThreads.append(
            threading.Thread(target=startTask)
        )
    # doTaskThread = threading.Thread(target=startTask)
    # doTaskThread.setDaemon(True)

    log.info(u'program start...')
    EXIT_CODE=0
    try:
        main()
    except KeyboardInterrupt:
        signal_handle('sigint')
    except:
        log.error(traceback.format_exc())
        EXIT_CODE = 1
    log.info(u"program quit...")
    sys.exit(EXIT_CODE)
