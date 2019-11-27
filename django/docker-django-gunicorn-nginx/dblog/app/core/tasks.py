# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task, task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

import psutil
import time
import json
import datetime
import netifaces
from django_redis import get_redis_connection
from collections import defaultdict, OrderedDict
from app.utils import network
from django.utils.translation import ugettext_lazy as _

DJANGO_CELERY_TCP_CONNECT_INFO = "dblog-celery-tcp-connect-info-{time}"
DJANGO_CELERY_TCP_CONNECT_INFO_SHOW = "dblog-celery-tcp-connect-info-show-{time}"

DJANGO_CELERY_NET_MONITOR_INFO = "dblog-celery-net-monitor-info-{network}-{time}"
DJANGO_CELERY_NET_MONITOR_INFO_SHOW = "dblog-celery-net-monitor-info-show-{network}-{time}"

KB = 1 << 10
MB = 1 << 20
GB = 1 << 30
TB = 1 << 40
PB = 1 << 50
EXPIRE_TIME = 3600*24*5
labelStep = 30

# ---------------------------
# TCP 连接情况
@shared_task(bind=False, ignore_result=True, store_errors_even_if_ignored=True)
def tcp_connect_info():
    """  统计 TCP连接情况
    netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'
    TIME_WAIT 8947 等待足够的时间以确保远程TCP接收到连接中断请求的确认
    FIN_WAIT1 15 等待远程TCP连接中断请求，或先前的连接中断请求的确认
    FIN_WAIT2 1 从远程TCP等待连接中断请求
    ESTABLISHED 55 代表一个打开的连接
    SYN_RECV 21 再收到和发送一个连接请求后等待对方对连接请求的确认
    CLOSING 2 没有任何连接状态
    LAST_ACK 4 等待原来的发向远程TCP的连接中断请求的确认

    TCP连接状态详解
    LISTEN： 侦听来自远方的TCP端口的连接请求
    SYN-SENT： 再发送连接请求后等待匹配的连接请求
    SYN-RECEIVED：再收到和发送一个连接请求后等待对方对连接请求的确认
    ESTABLISHED： 代表一个打开的连接
    FIN-WAIT-1： 等待远程TCP连接中断请求，或先前的连接中断请求的确认
    FIN-WAIT-2： 从远程TCP等待连接中断请求
    CLOSE-WAIT： 等待从本地用户发来的连接中断请求
    CLOSING： 等待远程TCP对连接中断的确认
    LAST-ACK： 等待原来的发向远程TCP的连接中断请求的确认
    TIME-WAIT： 等待足够的时间以确保远程TCP接收到连接中断请求的确认
    CLOSED： 没有任何连接状态

    https://blog.csdn.net/qadada/article/details/8423561
    http://www.echojb.com/coldfusion/2016/10/08/228099.html
    http://www.echojb.com/coldfusion/2016/10/08/228099.html

    https://my.oschina.net/u/1169079/blog/397705
    https://gist.github.com/ameizi/cb126be7383fb463eae8
    https://gist.github.com/ameizi/cb126be7383fb463eae8
    :return:
    """
    status_list = ["CLOSED", "CLOSE_WAIT", "CLOSING", "ESTABLISHED", "FIN_WAIT1", "FIN_WAIT2", "LAST_ACK", "LISTEN",
                   "SYN_RECV", "SYN_SENT", "TIME_WAIT"]
    fmt = time.strftime("%Y-%m-%d %H:%M")
    time_fmt1, time_fmt2 = fmt.split(" ")
    key = DJANGO_CELERY_TCP_CONNECT_INFO.format(time=time_fmt1)
    status_temp = []
    net_connections = psutil.net_connections()
    for k in net_connections:
        status_temp.append(k.status)

    status_result = []
    for status in status_list:
        status_result.append((
            status, status_temp.count(status) ))
    redis = get_redis_connection()
    d = json.dumps({ 'time': time_fmt2, "results": status_result })
    res = ( redis.pipeline()
            .lpush(key, d)
            .expire(key, EXPIRE_TIME)
            .lrange(key, 0, -1)
            .execute())

    # 缓存
    stat_cpu = res[-1]
    set_tcp_connect_info(redis, stat_cpu, time_fmt1)

def set_tcp_connect_info(redis, stat_cpu, fmt):
    key = DJANGO_CELERY_TCP_CONNECT_INFO_SHOW.format(time=fmt)
    stat_cpu = reversed(stat_cpu)
    categories = []
    datasets = defaultdict(list)
    for x in stat_cpu:
        x = json.loads(x)
        category = x['time']
        x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11 = x['results']
        categories.append(category)
        datasets['CLOSED'].append(x1[1])
        datasets['CLOSE_WAIT'].append(x2[1])
        datasets['CLOSING'].append(x3[1])
        datasets['ESTABLISHED'].append(x4[1])
        datasets['FIN_WAIT1'].append(x5[1])
        datasets['FIN_WAIT2'].append(x6[1])
        datasets['LAST_ACK'].append(x7[1])
        datasets['LISTEN'].append(x8[1])
        datasets['SYN_RECV'].append(x9[1])
        datasets['SYN_SENT'].append(x10[1])
        datasets['TIME_WAIT'].append(x11[1])
    datasets = dict(datasets)
    datasets_lists = []
    for k, v in datasets.iteritems():
        datasets_lists.extend(v)
    yaxisminValue = min(datasets_lists)
    # yaxisminValue = min([i for i in datasets_lists if i>0])
    yaxismaxValue = max(datasets_lists)
    redis.set(key, json.dumps({
        "datasets": datasets,
        "categories": categories,
        "yaxisminValue": yaxisminValue,
        "yaxismaxValue": yaxismaxValue,
    }))

def get_tcp_connect_info():
    now = datetime.datetime.now()
    before_now = now - datetime.timedelta(days=1)
    now_fmt = now.strftime("%Y-%m-%d")
    before_now_fmt = before_now.strftime("%Y-%m-%d")
    now_key = DJANGO_CELERY_TCP_CONNECT_INFO_SHOW.format(time=now_fmt)
    before_now_key = DJANGO_CELERY_TCP_CONNECT_INFO_SHOW.format(time=before_now_fmt)

    redis = get_redis_connection()
    now_tcp = _get_tcp_connect_info(redis, now_key)
    # before_now_tcp = _get_tcp_connect_info(redis, now_key, bn="bnow")
    before_now_tcp = _get_tcp_connect_info(redis, before_now_key, bn="bnow")
    return now_tcp, before_now_tcp

def _get_tcp_connect_info(redis, key, bn="now"):
    j = redis.get(key)
    if not j: return None
    d = json.loads(j)
    categories = d["categories"]
    # length = len(categories)
    # index = 0
    # while 1:
    #     if index>=length:break
    #     _c = categories[index]
    #     if _c.endswith(":00"):
    #         break
    #     index +=1
    datasets = d["datasets"]
    yaxisminValue = d["yaxisminValue"]
    yaxismaxValue = get_tcp_yaxismaxValue(d["yaxismaxValue"])
    category = "|".join(categories)
    dataset = []
    for status in ("CLOSED", "CLOSE_WAIT", "CLOSING", "ESTABLISHED", "FIN_WAIT1", "FIN_WAIT2", "LAST_ACK", "LISTEN", "SYN_RECV", "SYN_SENT", "TIME_WAIT"):
        data = datasets[status]
        dataset.append({
            "seriesname": status,
            "data": "|".join(map(str, data))
        })
    caption = _(u"今日TCP连接情况") % {}
    if bn=="bnow":
        caption = _(u"昨日TCP连接情况") % {}
    js = {
        'type': 'zoomline',
        'renderAt': 'tcp-info-container-{}'.format(bn),
        'width': '100%',
        'height': '500',
        'dataFormat': 'json',
        'dataSource': {
            "chart": {
                "caption": caption,  # 图表主标题
                "subcaption": "",  # 图表副标题
                "paletteColors": "#9585BF,#a90329,#3e7c8a,#c79121,#D6487E,#629B58,#ba43a9,#060AFE,#705da0,#cca300,#447ebc,#447ebc",
                # "paletteColors": "#7eb26d,#eab839,#3e7c8a,#ef843c,#e24d42,#1f78c1,#ba43a9,#705da0,#508642,#cca300,#447ebc,#447ebc",
                "captionFontSize": "16",
                "subcaptionFontSize": "16",
                "subcaptionFontBold": "0",
                "showBorder": "0",
                "bgColor": "#ffffff", # 图表背景色，6位16进制颜色值
                "canvasBgColor": "#1f1d1d",
                # "canvasBgColor": "#ffffff",  # 画布背景色，6位16进制颜色值
                # "bgColor": "#1f1d1d",
                "baseFont": "Helvetica Neue,Arial", # 图表字体样式
                "baseFontSize": "12", # 图表字体大小
                "showCanvasBorder": "0",
                "showShadow": "0",
                "showAlternateHGridColor": "0",
                "yaxisname": _(u"连接数") % {}, # 纵向坐标轴(y轴)名称
                "xaxisname": _(u"时间") % {}, # 横向坐标轴(x轴)名称
                "yaxisminValue": "{}".format(yaxisminValue),
                "yaxismaxValue": "{}".format(yaxismaxValue),
                "forceAxisLimits" : "1",
                "pixelsPerPoint": "0",

                "pixelsPerLabel": "12",  #间隔，每60分钟一个间隔

                "lineThickness": "1",
                "compactdatamode" : "1",
                "dataseparator" : "|",
                "labelHeight": "30",
                "scrollheight": "10",
                "flatScrollBars": "1",
                "scrollShowButtons": "0",
                "scrollColor": "#cccccc",
                "legendBgAlpha": "0",
                "legendBorderAlpha": "0",
                "legendShadow": "0",
                "legendItemFontSize": "14", # 项目字体大小
                "legendItemFontColor": "#666666",
                "formatNumberScale":"0",
                "showhovercap": True,
                "labelStep": "{}".format(labelStep),#间隔，每60分钟一个间隔
                # "numVDivLines": "12", # 垂直分割线
                # "numberSuffix": " KB/s",# 增加数字后缀
                # "numberPrefix": "KB/S", # 增加数字前缀     % 为 '%25'
                "numDivLines": 5,  # 水平分割线
            },
            "categories": [{
                "category":  "{}".format(category)
            }],
            "dataset": dataset
        }
    }
    return json.dumps(js)

# ---------------------------
# 监控网卡流量
@shared_task(bind=False, ignore_result=True, store_errors_even_if_ignored=True)
def network_monitor_info():
    key_info, net_in, net_out = network.get_nets_io_rate(network.get_nets_io)
    # time_fmt = time.strftime("%Y-%m-%d %H:%M")
    now = datetime.datetime.now()
    bnow_fmt = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    bbnow_fmt = (now - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    now_fmt_ = now.strftime("%Y-%m-%d %H:%M")
    now_fmt, time_fmt2 = now_fmt_.split(" ")
    redis = get_redis_connection()
    for k in key_info:
        key = DJANGO_CELERY_NET_MONITOR_INFO.format(network=k, time=now_fmt)
        _in = net_in.get(k)
        _out = net_out.get(k)
        d = json.dumps({'time': time_fmt2, "results": [_in, _out]})
        res = (redis.pipeline()
               .lpush(key, d)
               .expire(key, EXPIRE_TIME)
               # .ltrim(key, 0, 12*24*3)
               .lrange(key, 0, -1)
               .execute())
        stat_net = res[-1]
        set_network_monitor_info(redis, reversed(stat_net), k, now_fmt, bnow_fmt, bbnow_fmt)

def set_network_monitor_info(redis, nstat_net, net, now_fmt, bnow_fmt, bbnow_fmt):
    bkey = DJANGO_CELERY_NET_MONITOR_INFO.format(network=net, time=bnow_fmt)
    bbkey = DJANGO_CELERY_NET_MONITOR_INFO.format(network=net, time=bbnow_fmt)
    bstat_net = reversed(redis.lrange(bkey, 0, -1))
    bbstat_net = reversed(redis.lrange(bbkey, 0, -1))
    skey = DJANGO_CELERY_NET_MONITOR_INFO_SHOW.format(network=net, time=now_fmt)
    bskey = DJANGO_CELERY_NET_MONITOR_INFO_SHOW.format(network=net, time=bnow_fmt)
    bbskey = DJANGO_CELERY_NET_MONITOR_INFO_SHOW.format(network=net, time=bbnow_fmt)
    # stat_net = []
    # stat_net.extend(bbstat_net)
    # stat_net.extend(bstat_net)
    # stat_net.extend(nstat_net)
    for key, stats in [(skey, nstat_net),(bskey, bstat_net),(bbskey, bbstat_net)]:
        if not stats: continue
        categories = []
        datasets = defaultdict(list)
        for x in stats:
            x = json.loads(x)
            category = x['time']
            categories.append(category)
            x1, x2 = x['results']
            datasets['Incoming network traffic on {}'.format(net)].append(x1)
            datasets['Outgoing network traffic on {}'.format(net)].append(x2)
        datasets = dict(datasets)
        if not datasets: continue
        datasets_lists = []
        for k, v in datasets.iteritems():
            datasets_lists.extend(v)
        yaxisminValue = min(datasets_lists)
        # yaxisminValue = min([i for i in datasets_lists if i>0])
        yaxismaxValue = max(datasets_lists)
        ( redis.pipeline()
          .set(key, json.dumps({
            "datasets": datasets,
            "categories": categories,
            "yaxisminValue": yaxisminValue,
            "yaxismaxValue": yaxismaxValue,}))
          .expire(key, EXPIRE_TIME)
          .execute())

def get_network_monitor_info():
    key_info = network.get_nets()  # 获取网卡名称
    j = []
    keys = []
    redis = get_redis_connection()
    routingNicName = str(netifaces.gateways()['default'][netifaces.AF_INET][1])
    key_info.remove(routingNicName)
    key_info.insert(0, routingNicName)
    now = datetime.datetime.now()
    bnow_fmt = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    bbnow_fmt = (now - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    now_fmt = now.strftime("%Y-%m-%d")
    for k in key_info:
        d = _get_network_monitor_info(redis, k, now_fmt, bnow_fmt, bbnow_fmt)
        if d:
            keys.append(k)
            j.append( (k, d) )
    return keys, j

def _get_network_monitor_info(redis, net, now_fmt, bnow_fmt, bbnow_fmt):
    # key = DJANGO_CELERY_NET_MONITOR_INFO_SHOW.format(network=net, time=now_fmt)
    skey = DJANGO_CELERY_NET_MONITOR_INFO_SHOW.format(network=net, time=now_fmt)
    bskey = DJANGO_CELERY_NET_MONITOR_INFO_SHOW.format(network=net, time=bnow_fmt)
    bbskey = DJANGO_CELERY_NET_MONITOR_INFO_SHOW.format(network=net, time=bbnow_fmt)
    datajs = []
    days = [('today', _(u'今日'), skey, now_fmt), ('yest', _(u'昨日'), bskey, bnow_fmt), ('bday', _(u'前日'), bbskey, bbnow_fmt)]
    for daykey, day, key, day_fmt in days:
        j = redis.get(key)
        if not j:
            datajs.append((daykey, day, None))
            continue
        d = json.loads(j)
        categories = d["categories"]
        # length = len(categories)
        # index = 0
        # while 1:
        #     if index>=length:break
        #     _c = categories[index]
        #     if _c.endswith(":00"):
        #         break
        #     index +=1
        datasets = d["datasets"]
        yaxismaxValue = d["yaxismaxValue"]
        _unit, _unit_str, _unit_round = KB, 'KB/s', 1
        if yaxismaxValue>= MB:
            _unit, _unit_str, _unit_round  = MB, 'MB/s', 2
        yaxisminValue = 0
        yaxismaxValue = network.trans_io(d["yaxismaxValue"], _unit, _unit_round)
        yaxismaxValue = get_net_yaxismaxValue(yaxismaxValue, _unit)
        category = "|".join(categories)
        _in_key = 'Incoming network traffic on {}'.format(net)
        _out_key = 'Outgoing network traffic on {}'.format(net)
        _ins = [network.trans_io(i, _unit, _unit_round) for i in datasets[_in_key]]
        _outs = [network.trans_io(i, _unit, _unit_round) for i in datasets[_out_key]]
        dataset = [{
            "seriesname": _in_key,
            "data": "|".join(map(str, _ins))
        },{
            "seriesname": _out_key,
            "data": "|".join(map(str, _outs))
        }]
        caption = _(u'%(name)s网卡%(day)s流量监控') % {'name': net, "day": day_fmt}
        js = {
            'type': 'zoomline',
            'renderAt': 'net-info-container-{}-{}'.format(net, daykey),
            'width': '100%',
            'height': '500',
            'dataFormat': 'json',
            'dataSource': {
                "chart": {
                    "caption": caption,  # 图表主标题
                    "subcaption": "",  # 图表副标题
                    "paletteColors": "#c79121,#447ebc",
                    "captionFontSize": "16",
                    "subcaptionFontSize": "16",
                    "subcaptionFontBold": "0",
                    "showBorder": "0",
                    "bgColor": "#ffffff", # 图表背景色，6位16进制颜色值
                    "canvasBgColor": "#1f1d1d",
                    # "canvasBgColor": "#ffffff",  # 画布背景色，6位16进制颜色值
                    # "bgColor": "#1f1d1d",
                    "baseFont": "Helvetica Neue,Arial", # 图表字体样式
                    "baseFontSize": "12", # 图表字体大小
                    "showCanvasBorder": "0",
                    "showShadow": "0",
                    "showAlternateHGridColor": "0",
                    "yaxisname": _(u"流量") % {}, # 纵向坐标轴(y轴)名称
                    "xaxisname": _(u"时间") % {}, # 横向坐标轴(x轴)名称
                    "yaxisminValue": "{}".format(yaxisminValue),
                    "yaxismaxValue": "{}".format(yaxismaxValue),
                    "forceAxisLimits" : "1",
                    "pixelsPerPoint": "0",

                    "pixelsPerLabel": "12",  #间隔，每60分钟一个间隔

                    "lineThickness": "1",
                    "compactdatamode" : "1",
                    "dataseparator" : "|",
                    "labelHeight": "30",
                    "scrollheight": "10", #
                    "flatScrollBars": "1",
                    "scrollShowButtons": "0",
                    "scrollColor": "#cccccc",
                    "legendBgAlpha": "0",
                    "legendBorderAlpha": "0",
                    "legendShadow": "0",
                    "legendItemFontSize": "14", # 项目字体大小
                    "legendItemFontColor": "#666666",
                    "formatNumberScale":"0",
                    "showhovercap": True,
                    "labelStep": "{}".format(labelStep),  # 间隔，每60分钟一个间隔
                    # "numVDivLines": "12", # 垂直分割线
                    "numberSuffix": _unit_str,# 增加数字后缀
                    # "numberPrefix": "KB/S", # 增加数字前缀     % 为 '%25'
                    "numDivLines": 5, # 水平分割线
                },
                "categories": [{
                    "category":  "{}".format(category)
                }],
                "dataset": dataset
            }
        }
        datajs.append((daykey, day, json.dumps(js)))
    return datajs

def get_tcp_yaxismaxValue(yaxismaxValue):
    if yaxismaxValue>200:
        d = 150
        while 1:
            if d >= yaxismaxValue:
                return d
            d += 30
    else:
        d = 60
        while 1:
            if d >= yaxismaxValue:
                return d
            d += 30

def get_net_yaxismaxValue(yaxismaxValue, unit):
    if unit == MB:
        d = 1.2
        while 1:
            if d>=yaxismaxValue:
                return d
            d += 0.3
    else:
        if yaxismaxValue>=30:
            d = u = 30
        else:
            d = u = 3
        while 1:
            if d >= yaxismaxValue:
                return d
            d += u