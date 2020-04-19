#!/usr/bin/python
#coding=utf8
import getopt
import json
import datetime
import ipaddr
import time
import redis
import sys

__author__ = 'leo'


import os
import redis
import ipaddr
import json


def dump_ip():
    path = './'

    os.popen("""mysql -h202.103.191.118 -umm-app -phcMVxw7aDdJracy \
             -P62401 -e "select address from core_server" mm-ms > %s""" % os.path.join(path, 'check_ip_list.txt'))

    ip_list = open(os.path.join(path, 'check_ip_list.txt'), 'rb').readlines()

    insert_list = []
    for each_ip in ip_list:
        try:
            ip = ipaddr.IPv4Address(each_ip.strip())
        except ipaddr.AddressValueError:
            continue
        if ip.is_private or ip.is_loopback:
            continue
        insert_list.append(each_ip.strip())
    return insert_list


def add_core_ip(r):
    insert_list = dump_ip()

    for e in insert_list:
        print e
        r.lpush('U-mail', e)
        r.lpush('checklist', e)


def drop_redis_data(r):

    pbl_ips = r.smembers('pbl_ips')
    xbl_ips = r.smembers('xbl_ips')
    sbl_ips = r.smembers('sbl_ips')
    l = json.dumps({'pbl_ips': list(pbl_ips), 'sbl_ips': list(sbl_ips), 'xbl_ips': list(xbl_ips)})
    r.set('blocklist', l)

    r.delete('pbl_ips', 'xbl_ips', 'sbl_ips', 'dispatch', 'task_checked', 'U-mail', 'task_dispatch', 'task_finished')


def validate(ip):
    try:
        ip = ipaddr.IPv4Address(ip)
    except ipaddr.AddressValueError:
        return False
    return ip


def get_datetime(date_str):

    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M")))


def task_failed_retry(r):
    """
    任务重试
    """
    in_dispatch = r.smembers('dispatch')
    for ip in in_dispatch:
        detail = r.hget('task_dispatch', ip)
        # print detail
        detail = json.loads(detail)
        # print detail
        d = get_datetime(detail['create_dtm'])

        # 任务10分钟之内没完成则重试
        if (datetime.datetime.now() - d).total_seconds() > 600:
            r.srem('dispatch', ip)
            if validate(ip):
                r.lpush('task', ip)


def add_task(r):
    """
    添加任务
    """
    # 检测在pbl列表的隔天检测一次
    pbl_ip_check_interval = 60 * 60 * 3
    # 普通IP两天检测一次
    normal_interval = 60 * 60 * 6

    now = datetime.datetime.now()

    check_history = r.hgetall('task_checked')
    pbl_list = r.smembers('pbl_ips')
    for ip, info in check_history.items():
        info = json.loads(info)
        if (ip in pbl_list) and (now - get_datetime(info['create_dtm'])).total_seconds() > pbl_ip_check_interval:
            if validate(ip) and ip not in r.lrange('checklist', 0, -1):
                r.lpush('checklist', ip)

        elif (now - get_datetime(info['create_dtm'])).total_seconds() > normal_interval:
            if validate(ip) and ip not in r.lrange('checklist', 0, -1):
                r.lpush('checklist', ip)


if __name__ == "__main__":

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["REDIS_DB_HOST=", "REDIS_DB_PORT=", "REDIS_DB_NAME="])
    except getopt.GetoptError as err:
        print "schedule script parse argument error"
        sys.exit(0)

    options = {}
    for k, v in opts:
        k = k.strip("--")
        if k == "REDIS_DB_PORT":
            options[k] = int(v)
        else:
            options[k] = v

    pool = redis.ConnectionPool(host=options['REDIS_DB_HOST'], port=options['REDIS_DB_PORT'],
                                db=options['REDIS_DB_NAME'])
    cli = redis.Redis(connection_pool=pool)

    #task_failed_retry(cli)
    #add_task(cli)

    drop_redis_data(cli)

    add_core_ip(cli)

    # 关闭连接
    pool.disconnect()
