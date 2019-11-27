# -*- coding: utf-8 -*-
#
import os
from django.conf import settings
# from django_sysinfo.conf import PROCESSES

LOGTAIL_UPDATE_INTERVAL = getattr(settings, 'LOGTAIL_UPDATE_INTERVAL', '3000')


LOGTAIL_FILES = {
    'celerybeat': "/usr/local/log/dblog/dblog-celery-beat.log",
    'celeryworker': "/usr/local/log/dblog/dblog-celery-worker.log",
    'apache': "/usr/local/log/dblog/dblog_apache.log",
    'apache_error': "/usr/local/log/dblog/dblog_apache_error.log",
    'nginx': "/usr/local/log/dblog/dblog_nginx.log",
    'nginx_error': "/usr/local/log/dblog/dblog_nginx_erorr.log",
}

# for k, v in PROCESSES.iteritems():
#     filepath = v.get('log', '')
#     if os.path.exists(filepath):
#         LOGTAIL_FILES[k] = filepath

# def get_logtail_files():
#     LOGTAIL_FILES = getattr(settings, 'LOGTAIL_FILES', {})
#     for c in Cluster.objects.all():
#         LOGTAIL_FILES[c.name] = os.path.join(DEPLOY_DIR, 'log', 'deploy_%s.log' % c.id)
#         LOGTAIL_FILES[str(c.id)] = (c.name, os.path.join(DEPLOY_DIR, 'log', 'deploy_%s.log' % c.id))
#         LOGTAIL_FILES['m_{}'.format(c.id)] = (c.name, os.path.join(MONITOR_DIR, 'log', 'monitor_%s.log' % c.id))
#     # LOGTAIL_FILES['register'] = (c.name, os.path.join(TROY_DIR, 'log', 'qq_register.log'))
#     return LOGTAIL_FILES
