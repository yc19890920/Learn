#!/usr/bin/python
#coding=utf8
import ipaddr
import tornadoredis
import json
import datetime
from tornado import gen


__author__ = 'leo'


def get_ip_list_from_net(net):
    """
    网段: net: '211.195.0.0/24'
    """
    try:
        net = ipaddr.IPv4Network(net)
    except ipaddr.AddressValueError:
        return []

    return [ip for ip in net.iterhosts() if not (ip.is_private or ip.is_loopback)]


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M")

        return json.JSONEncoder.default(self, o)


class Customer(object):

    def __init__(self, handler):

        self.handler = handler
        self.pool = self.handler.settings['CONNECTION_POOL']

    @gen.engine
    def add_customer(self, name, callback=None):
        c = tornadoredis.Client(connection_pool=self.pool)
        exist_or_not = yield gen.Task(c.sismember, 'customer', name)
        if exist_or_not:
            yield gen.Task(c.disconnect)
            callback(False, u'客户已经存在')
        else:
            yield gen.Task(c.sadd, 'customer', name)
            yield gen.Task(c.disconnect)
            callback(True, u'添加成功')

    @gen.engine
    def rename_customer(self, name, new_name, callback=None):
        c = tornadoredis.Client(connection_pool=self.pool)
        res = yield gen.Task(c.srem, 'customer', name)
        if res:
            yield gen.Task(c.rename, u'c_%s' % name, u'c_%s' % new_name)
            yield gen.Task(c.disconnect)
            callback(True, u'重命名成功')
        else:
            callback(False, u'重命名失败')

    @gen.coroutine
    def delete_customer(self, name):
        c = tornadoredis.Client(connection_pool=self.pool)
        yield gen.Task(c.srem, 'customer', name)
        yield gen.Task(c.delete, u'c_%s' % name)

    @gen.engine
    def add_ips(self, name, ip_list, callback=None):
        c = tornadoredis.Client(connection_pool=self.pool)
        valid_name = yield gen.Task(c.sismember, 'customer', name)
        yield gen.Task(c.disconnect)

        if not valid_name:
            callback(False)
        else:
            c = tornadoredis.Client(connection_pool=self.pool)
            pipe = c.pipeline()
            for ip in ip_list:
                print 'list', ip
                pipe.sadd(u'c_%s' % name, ip)
                for each in get_ip_list_from_net(ip):
                    print each, "add"
                    pipe.lpush('task', each)
            yield gen.Task(pipe.execute)
            yield gen.Task(c.disconnect)

            # 将IP直接放入task队列等待处理
            callback(True)

    @gen.engine
    def get_ips(self, name='', callback=None):
        if not bool(name):
            c = tornadoredis.Client(connection_pool=self.pool)
            customer = yield gen.Task(c.smembers, 'customer')
            data_list = []
            for name in customer:
                ips = yield gen.Task(c.smembers, u'c_%s' % name)
                data_list.append({'name': name, 'data_list': {'ips': ips, 'num': len(ips)}})

            yield gen.Task(c.disconnect)
            callback(data_list)
        else:
            c = tornadoredis.Client(connection_pool=self.pool)
            ips = yield gen.Task(c.smembers, u'c_%s' % name)
            callback([{'name': name, 'data_list': {'ips': ips, 'num': len(ips)}}])

    @gen.coroutine
    def delete_ip(self, name, ip):
        c = tornadoredis.Client(connection_pool=self.pool)
        pipe = c.pipeline()
        pipe.srem(u'c_%s' % name, ip)
        for ip in get_ip_list_from_net(ip):
            pipe.lrem('task', 0, ip)
            pipe.srem('dispatch', ip)
            pipe.srem('pbl_ips', ip)
            pipe.srem('xbl_ips', ip)
            pipe.srem('sbl_ips', ip)
            pipe.hdel('task_dispatch', ip)
            pipe.hdel('task_checked', ip)
            pipe.hdel('task_finished', ip)
            yield gen.Task(pipe.execute)
        yield gen.Task(c.disconnect)
