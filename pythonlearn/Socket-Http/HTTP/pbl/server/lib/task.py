#!/usr/bin/python
#coding=utf8
import ipaddr
import tornadoredis
import json
import datetime
import time
from tornado import gen

__author__ = 'leo'


def get_datetime(date_str):

    return datetime.datetime.fromtimestamp(time.mktime(time.strptime(date_str, "%Y-%m-%d %H:%M")))


def get_ip_list_from_net(net):
    """
    网段: net: '211.195.0.0/24'
    """
    try:
        net = ipaddr.IPv4Network(net)
    except ipaddr.AddressValueError:
        return []

    if net.prefixlen == 32:
        return [net.ip]
    else:
        return [ip for ip in net.iterhosts() if not (ip.is_private or ip.is_loopback)]



def validate(ip):
    try:
        ip = ipaddr.IPv4Address(ip)
    except ipaddr.AddressValueError:
        return False
    return ip


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M")

        return json.JSONEncoder.default(self, o)


class Task(object):
    def __init__(self, handler):

        self.handler = handler
        self.pool = self.handler.settings['CONNECTION_POOL']

    @gen.engine
    def get_check(self, callback=None):
        c = tornadoredis.Client(connection_pool=self.pool)
        while True:
            task = yield gen.Task(c.blpop, 'checklist')
            if task:
                ip = task['checklist']
                if validate(ip):
                    break
        # ip = "127.0.0.2"
        yield gen.Task(c.disconnect)
        callback(ip)

    @gen.coroutine
    def add_task(self, ip):
        c = tornadoredis.Client(connection_pool=self.pool)
        yield gen.Task(c.lpush, 'task', ip)
        yield gen.Task(c.disconnect)

    @gen.engine
    def get_task(self, callback=None):
        c = tornadoredis.Client(connection_pool=self.pool)
        while True:
            task = yield gen.Task(c.blpop, 'task')
            if task:
                ip = task['task'] 
                if validate(ip):
                    break
        yield gen.Task(c.sadd, 'dispatch', ip)
        yield gen.Task(c.disconnect)
        yield self.change_task_status(ip, 'dispatch', {})
        callback(ip)

    def get_task_detail(self):
        pass

    @gen.coroutine
    def change_task_status(self, ip, status, info={}):
        assert validate(ip)
        assert isinstance(info, dict)
        info.update({'create_dtm': datetime.datetime.now(), 'ip': ip})
        dump_info = JSONEncoder().encode(info)

        if status == 'dispatch':
            c = tornadoredis.Client(connection_pool=self.pool)
            yield gen.Task(c.hset, 'task_dispatch', ip, dump_info)
            yield gen.Task(c.disconnect)
        elif status == 'checked':
            c = tornadoredis.Client(connection_pool=self.pool)
            if gen.Task(c.sismember, 'dispatch', ip):
                yield gen.Task(c.hset, 'task_checked', ip, dump_info)
                if info['PBL'] == '1':
                    yield gen.Task(c.sadd, 'pbl_ips', ip)
                if info['SBL'] == '1':
                    yield gen.Task(c.sadd, 'sbl_ips', ip)
                if info['XBL'] == '1':
                    yield gen.Task(c.sadd, 'xbl_ips', ip)
                yield gen.Task(c.srem, 'dispatch', ip)
            yield gen.Task(c.disconnect)
        elif status == 'finished':
            c = tornadoredis.Client(connection_pool=self.pool)
            pipe = c.pipeline()
            pipe.hset('task_finished', ip, dump_info)
            pipe.srem('dispatch', ip)
            yield gen.Task(pipe.execute)
            yield gen.Task(c.disconnect)

    @gen.engine
    def get_report(self, callback=None):
        c = tornadoredis.Client(connection_pool=self.pool)
        report_keys = yield gen.Task(c.keys, 'report*')
        report_list = yield gen.Task(c.mget, report_keys)
        # 任务队列情况
        task_num = yield gen.Task(c.llen, 'task')
        dispatch_num = yield gen.Task(c.scard, 'dispatch')

        checked_num = yield gen.Task(c.hlen, 'task_checked')
        finished_num = yield gen.Task(c.hlen, 'task_finished')

        pbl_ips = yield gen.Task(c.scard, 'pbl_ips')
        sbl_ips = yield gen.Task(c.scard, 'sbl_ips')
        xbl_ips = yield gen.Task(c.scard, 'xbl_ips')

        email_check_num = yield gen.Task(c.scard, 'email_check')

        yield gen.Task(c.disconnect)

        new_report_list = []
        report_list = [json.loads(each) for each in report_list]
        for report in report_list:
            report['create_dtm'] = get_datetime(report['create_dtm'])
            new_report_list.append(report)
        report_list = sorted(new_report_list, key=lambda item: item['create_dtm'], reverse=True)

        callback({"task_num": task_num, 'email_check_num': email_check_num,
                  "dispatch_num": dispatch_num,
                  "checked_num": checked_num, "finished_num": finished_num,
                  "pbl_ips": pbl_ips, "sbl_ips": sbl_ips, "xbl_ips": xbl_ips,
                  "report_list": report_list[:100]})

    @gen.engine
    def get_blocklist(self, callback=None):
        c = tornadoredis.Client(connection_pool=self.pool)
        blocklist = yield gen.Task(c.get, 'blocklist')
        yield gen.Task(c.disconnect)
        callback(json.loads(blocklist))

    @gen.coroutine
    def receive_report(self, info):
        remote_ip = self.handler.request.remote_ip
        info.update({'create_dtm': datetime.datetime.now(), 'remote_ip': remote_ip})
        dump_info = JSONEncoder().encode(info)

        c = tornadoredis.Client(connection_pool=self.pool)
        pipe = c.pipeline()
        key = 'report_%s' % time.time()

        pipe.set(key, dump_info)
        pipe.expire(key, 60*60*24*4)
        yield gen.Task(pipe.execute)
        yield gen.Task(c.disconnect)

    @gen.engine
    def get_ips(self, callback=None):
        """
        查看 PBL_Killer 监控的所有IP地址
        """
        c = tornadoredis.Client(connection_pool=self.pool)
        ips_dict = yield gen.Task(c.hgetall, 'ips')
        yield gen.Task(c.disconnect)

        ips_list = [{'name': k, 'ips': json.loads(v), 'num': len(json.loads(v))} for k, v in ips_dict.items() \
                    if k not in ['U-mail']]
        callback(ips_list)

    @gen.engine
    def get_umail_ips(self, callback=None):
        """
        查看 PBL_Killer 监控的所有IP地址
        """
        c = tornadoredis.Client(connection_pool=self.pool)
        ips_list = yield gen.Task(c.smembers, 'U-mail')
        yield gen.Task(c.disconnect)

        callback({'name': 'U-mail', 'num': len(ips_list), 'ips': ips_list})


@gen.coroutine
def check_task_queue(ioloop, app):
    pool = app.settings['CONNECTION_POOL']
    c = tornadoredis.Client(connection_pool=pool)
    num = yield gen.Task(c.llen, 'task')
    yield gen.Task(c.disconnect)
    print "Task num is: ", num
