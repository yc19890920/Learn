# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

import logging
import os
import socket
import datetime
import copy
from collections import OrderedDict

import psutil
from pkg_resources import get_distribution
import six
from django.conf import settings
from django.utils.module_loading import import_string

from django_sysinfo.utils import get_network, humanize_bytes
from django_redis import get_redis_connection
from .conf import config, PROCESSES
from lib.tools import getFileSize


logger = logging.getLogger(__name__)

UNKNOWN = "unknown"


def get_host(**kwargs):
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk_partitions = psutil.disk_partitions()
    host = OrderedDict()
    host["hostname"] = socket.gethostname()
    host["fqdn"] = socket.getfqdn()

    host["memory"] = {"total": humanize_bytes(mem.total),
                      "available": humanize_bytes(mem.available),
                      "percent": mem.percent,
                      "used": humanize_bytes(mem.used),
                      "free": humanize_bytes(mem.free),
                      "buffers": humanize_bytes(mem.buffers),
                      "cached": humanize_bytes(mem.cached),
    }

    host["swap"] = {"total": humanize_bytes(swap.total),
                    "percent": swap.percent,
                    "used": humanize_bytes(swap.used),
                    "free": humanize_bytes(swap.free)
    }
    disks = []

    for a in disk_partitions:
        disk = a.__dict__
        d = psutil.disk_usage(a.mountpoint)
        disk['total'] = humanize_bytes(d.total)
        disk['used'] = humanize_bytes(d.used)
        disk['free'] = humanize_bytes(d.free)
        disk['percent'] = d.percent
        disks.append(disk)
    host["disk"] = disks

    return host


def get_os(**kwargs):
    system_path = '/etc/redhat-release'
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    td = datetime.datetime.now() - boot_time
    return {
        "system_name": open(system_path, 'r').read() if os.path.exists(system_path) else '',
        "uname": os.uname(),
        "name": os.name,
        "boot_time": boot_time,
        "delta_time": u'{}天 {}小时 {}分钟'.format(td.days, td.seconds // 3600, (td.seconds // 60) % 60),
        "users": psutil.users(),
        "avg_load": os.getloadavg(),
        "cpus": psutil.cpu_count(),
        "cpu_percent": psutil.cpu_times_percent(),
        "network": get_network(),
        "pids": len(psutil.pids())
    }

def get_processes(**kwargs):
    name = kwargs.get('name', '')
    processes = copy.deepcopy(PROCESSES)
    if name and name in processes.keys():
        processes = {name: processes.get(name, {})}
    for p in psutil.process_iter(attrs=['pid', 'ppid', 'name', 'exe', 'cpu_percent', 'memory_percent', 'create_time', 'cmdline']):
        for k, v in processes.iteritems():
            if p.info['cmdline'] and [l for l in p.info['cmdline'] if v['cmd'] in l]:
                if k == 'httpd' and p.info['ppid'] != 1:
                    continue
                processes[k].update(p.info)
    return processes

def get_queues(**kwargs):
    redis = get_redis_connection()
    res = OrderedDict()
    queue_names = ['router', 'postman', 'smtp', 'incheck', 'maillist', 'forward', 'dkim', 'review']
    for n in queue_names:
        lock_key = 'task_lock:' + n
        wait_key = 'task_queue:' + n
        file_path = os.path.join('/usr/local/u-mail/app/data/', 'cache_{}'.format(n))
        res[n] = {
            'wait': redis.llen(wait_key),
            'lock': redis.scard(lock_key),
            'size': humanize_bytes(getFileSize(file_path))
        }
    return res


def run_check(id, request=None, fail_silently=True, fail_status=500):
    status = 200
    try:
        v = config.checks[id]
        if isinstance(v, six.string_types):
            c = import_string(v)
            ret, status = c(request)
        elif callable(v):
            ret, status = v(request)
        else:
            ret = v
    except Exception as e:
        ret = "ERROR"
        status = fail_status
        logger.exception(e)
        if settings.DEBUG:
            ret = str(e)
        if not fail_silently:
            raise

    return ret, status


def get_checks(request=None):
    checks = {}
    if config.checks:
        for k, v in config.checks.items():
            checks[k] = run_check(k)

    return checks


def get_extra(config, request=None):
    extras = {}
    for k, v in config.extra.items():
        try:
            if isinstance(v, six.string_types):
                c = import_string(v)
                extras[k] = c(request)
            elif callable(v):
                extras[k] = v(request)
            else:
                extras[k] = v
        except Exception as e:
            logger.exception(e)
            if settings.DEBUG:
                extras[k] = str(e)
    return extras


handlers = OrderedDict([("host", get_host),
                        ("os", get_os),
                        ("extra", get_extra),
                        ("checks", get_checks),
                        ("processes", get_processes),
                        ("queues", get_queues)
                        ])

valid_sections = handlers.keys()


def get_sysinfo(request):
    data = OrderedDict()
    sections = request.GET.get("s", None)
    if sections is None:
        sections = valid_sections
    else:
        sections = sections.split(",")

    for section in sections:
        if section in valid_sections and getattr(config, section):
            data[section] = handlers[section](config=config, request=request)

    return data


def get_version(name):
    try:
        version = get_distribution(name).version
    except:
        version = UNKNOWN
    return version
