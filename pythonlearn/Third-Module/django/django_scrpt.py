# -*- coding: utf-8 -*-
#

" django模块导入作为脚本，结合gevent "

from gevent import monkey
monkey.patch_all()

import gevent
import gevent.pool

import os
import re
import sys
import signal
import json
import datetime
import traceback

import django
ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../django_demo'))
SCRIPT = os.path.join(ROOT, 'script')
# 添加django工程路径
sys.path.append(ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_demo.settings")
django.setup()

from django.db import InterfaceError, DatabaseError, connections
from django.db.models import F, Sum, Q
from django.conf import settings
from django_redis import get_redis_connection
from django.core.exceptions import ObjectDoesNotExist

import logging
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))

log = logging.getLogger('Test')
log.addHandler(_handler)
log.setLevel(logging.DEBUG)

redis = get_redis_connection()

signal_stop = False

# ###########################################################
def do_worker1(task_id):
    log.info('-------do_worker1-------')
    return

def worker1():
    while True:
        if signal_stop: break
        _, task_id = redis.brpop(settings.EDMWEB_NULL_TEMPLATE_QUEQUE)
        try:
            do_worker1(task_id)
            gevent.sleep(0.5)
        except ObjectDoesNotExist:
            log.error(traceback.format_exc())
            gevent.sleep(0.1)
        except (DatabaseError, InterfaceError), e:
            redis.rpush(settings.EDMWEB_NULL_TEMPLATE_QUEQUE, task_id)
            log.error(traceback.format_exc())
            reconnect('dbname')
            gevent.sleep(0.1)
        except BaseException as e:
            log.error(traceback.format_exc())
            gevent.sleep(0.1)


# ###########################################################
def do_worker2():
    log.info('-------do_worker2-------')
    return

def worker2():
    pool = gevent.pool.Pool(50)
    while True:
        if signal_stop: break
        pool.spawn(do_worker2)
        gevent.sleep(0.1)
    pool.join()



# ###########################################################
def reconnect(dbname):
    try:
        log.info('reconnect {} start'.format(dbname))
        cursor = connections[dbname].cursor()
        db = cursor.db
        if db.connection is None or not db.is_usable():
            db.close_if_unusable_or_obsolete()
            with db.wrap_database_errors:
                db.connect()
            log.info(u'reconnect {} end'.format(dbname))
            gevent.sleep(10)
    except Exception as e:
        log.warning(u'DB Connection error', exc_info=1)

def get_connect_cr(dbname):
    cr = connections[dbname].cursor()
    db = cr.db
    if db.connection is None or not db.is_usable():
        db.close_if_unusable_or_obsolete()
        with db.wrap_database_errors:
            db.connect()
        cr = connections[dbname].cursor()
        log.info(u'reconnect {} get end'.format(dbname))
    return cr

############################################################
# 信号量处理
def signal_handle(mode):
    log.info("catch signal: %s" % mode)
    global signal_stop
    signal_stop = True

# 设置程序结束信号量
def init_gevent_signal(handler):
    gevent.signal(signal.SIGINT, handler, 'sigint')  # 处理 Ctrl-C
    gevent.signal(signal.SIGTERM, handler, 'sigterm')  # 处理 kill
    gevent.signal(signal.SIGALRM, handler, 'sigalrm')  # 处理 signal.alarm()

# ###########################################################
def init():
    log.info('init...')

def finish():
    log.info('finish...')

def main():
    gevent.spawn(worker1)
    worker2()

if __name__ == "__main__":
    # 运行程序
    EXIT_CODE = 0
    log.info(u'program start...')
    init_gevent_signal(signal_handle)
    init()
    EXIT_CODE = 0
    try:
        main()
    except KeyboardInterrupt:
        signal_handle('sigint')
    except:
        log.error(traceback.format_exc())
        EXIT_CODE = 1
    finally:
        finish()
    log.info(u"program quit...")
    sys.exit(EXIT_CODE)

