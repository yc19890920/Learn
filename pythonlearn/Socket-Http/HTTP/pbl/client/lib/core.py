# -*- coding: utf-8 -*-
#

import sys
import requests
import socket
import random
import time
import traceback
import gevent.local

from pbl_configs import HOST, MAIL_ADDRESS, HEADERS, UA
from pbl_spider import check_ip, process

local = gevent.local.local()

original_create_connection = socket.create_connection

def new_create_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
    if source_address is None and hasattr(local, 'ip'):
        source_address = (local.ip, 0)
    return original_create_connection(address, timeout, source_address)

socket.create_connection = new_create_connection

def clean(bound_ip=None, clear_ip=None):
    local.ip = bound_ip or "127.0.0.1"
    ip = clear_ip
    print >> sys.stdout, 'local ip: {}, clean ip: {}'.format(local.ip, ip)

    session = requests.session()
    session.headers.update(HEADERS)
    session.headers.update({'User-Agent': random.choice(UA)})

    # 检测IP是否在黑名单, result格式: (PBL, SBL, XBL)   在对应黑名单中置1, 否则置0
    result = check_ip(session, ip)
    PBL, SBL, XBL, check_result_html_page = result
    time.sleep(3)

    if PBL == '1':
        try:
            status, info = process(session, ip, MAIL_ADDRESS)
            return status, info
        except Exception, e:
            print >> sys.stderr, traceback.format_exc()
            return False, "clean exception"
    return False, "not in the PBL"


if __name__ == "__main__":
    status, info = clean(bound_ip="192.168.1.24", clear_ip="61.144.162.30")
    print status
    print info






