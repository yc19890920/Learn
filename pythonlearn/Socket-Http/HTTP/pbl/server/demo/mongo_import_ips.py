#!/usr/bin/python
#coding=utf8
import os
import datetime
import ipaddr
import pymongo

__author__ = 'leo'

path = '/tmp/'

# os.popen("""mysql -h202.103.191.118 -umm-ss -p4KdDgdutoKSdDxX \
#         -P62401 -e "select address from core_server" mm-ms > %s""" % os.path.join(path, 'check_ip_list.txt'))


ip_list = open(os.path.join(path, 'check_ip_list.txt'), 'rb').readlines()

insert_list = []
for each_ip in ip_list:
    try:
        ip = ipaddr.IPv4Address(each_ip.strip())
    except ipaddr.AddressValueError:
        continue

    if ip.is_private or ip.is_loopback:
        continue

    insert_list.append({'ip': each_ip.strip(), 'company_id': 1, 'create_dtm': datetime.datetime.now()})

mongo = pymongo.MongoClient(host='localhost', port=27017, use_greenlets=True)
db = mongo.pbl_killer

if insert_list:
    # db.ips.insert(insert_list)
    for e in insert_list:
        try:
            db.task.insert({"_id": e['ip']})
        except:
            continue
else:
    print "insert_list is empty"
