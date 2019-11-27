# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
# celery 定时任务
from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # TCP连接情况
    'tcp_connect_info': {
        'task': 'app.core.tasks.tcp_connect_info',
        'schedule': crontab(minute="*/2"),
        'args': ()
    },

    # 网卡流量监控
    'network_monitor_info': {
        'task': 'app.core.tasks.network_monitor_info',
        'schedule': crontab(minute="*/2"),
        'args': ()
    },
}
