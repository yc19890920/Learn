#!/usr/bin/python
#coding=utf8
import os
import redis
import ipaddr
import json
__author__ = 'leo'

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


pool = redis.ConnectionPool(host='localhost', port=6377, db=0)
r = redis.Redis(connection_pool=pool)

# print len(insert_list)
# while r.llen('task'):
#     r.rpop('task')

for e in insert_list:
    print e
    r.lpush('U-mail', e)
    r.lpush('task', e)


