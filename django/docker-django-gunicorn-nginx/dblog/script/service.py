# -*- coding: utf-8 -*-
#

from gevent import monkey
monkey.patch_all()

import gevent
import os
import re
import sys
import json
import traceback

import django
ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '../../dblog'))
SCRIPT = os.path.join(ROOT, 'script')
sys.path.append(ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dblog.settings")
django.setup()

from django_redis import get_redis_connection
from django.conf import settings
from django.db import InterfaceError, DatabaseError, connections

from libs.signals import init_gevent_signal
from libs.email import send_email
from libs.email import make_email
from libs.formats import dict_compatibility
from libs import tools
from libs.log import getLog
log = getLog("service")
redis = get_redis_connection()
signal_stop=False

#  邮件通知队列， 注册、系统，注册优先级最高
EMAIL_REGISTER_KEY = "email:register"
EMAIL_SYSTEM_KEY = "email:system"
MAIL_KEYS = [EMAIL_REGISTER_KEY, EMAIL_SYSTEM_KEY]

############################################################
# 发送邮件
def _sendEmail(j):
    receiver, subject, content = j["receiver"], j["subject"], j["content"]
    host, port, is_ssl, account, password = tools.getSmtpAccout()
    s = send_email.MailSender()
    index=5
    while index:
        code, msg = s.send_email(host, port, account, password, receiver, subject, content, ssl=is_ssl)
        if code == 250:
            log.info(u'notice success')
            break
        else:
            index -= 1
            log.error(u'notice error, index: {}'.format(5-index))
            log.error(traceback.format_exc(), exc_info=1)

def sendEmail():
    while True:
        if signal_stop: break
        _, d = redis.brpop(MAIL_KEYS)
        try:
            _sendEmail( json.loads(d) )
        except (DatabaseError, InterfaceError) as e:
            # 如果报数据库异常，关闭连接，重新处理任务
            redis.lpush(EMAIL_SYSTEM_KEY, d)
            log.warning(u'DatabaseError', exc_info=1)
            reconnect()
        except BaseException as e:
            log.error(traceback.format_exc())

############################################################
def init():
    pass

def main():
    init()
    init_gevent_signal(signal_handle)
    gevent.joinall([
        gevent.spawn(sendEmail),
        gevent.spawn(sendEmail),
    ])

############################################################

def reconnect():
    try:
        log.info('Restoring the Mysql Connection start')
        cursor = connections['mm-ms'].cursor()
        db = cursor.db
        # assert issubclass(db.__class__, BaseDatabaseWrapper)
        if db.connection is None or not db.is_usable():
            db.close_if_unusable_or_obsolete()
            with db.wrap_database_errors:
                db.connect()
            log.info('Restoring the Mysql Connection end')
            gevent.sleep(5)
    except Exception as e:
        log.warning('DB Connection error', exc_info=1)

# 信号量处理
def signal_handle(mode):
    log.info("catch signal: %s" % mode)
    global signal_stop
    signal_stop = True

if __name__ == "__main__":
    log.info("program start...")
    main()
    log.info("program quit...")
