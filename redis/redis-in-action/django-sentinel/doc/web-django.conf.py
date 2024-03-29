# -*-coding:utf-8 -*-
__author__ = "YC"

import os
import multiprocessing

BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', "django-sentinel"))
#
chdir = BASE_DIR

# 监听本机的5000端口
# bind = '127.0.0.1:10000'
bind = '0.0.0.0:10086'

# 开启进程
# workers = 8 # multiprocessing.cpu_count() * 2 + 1
workers = multiprocessing.cpu_count() * 2 + 1

# 每个进程的开启线程
threads = 30

# 等待连接的最大数
backlog = 2048
# 最大客户端并发数量，默认1000
worker_connections = 2000

#工作模式为meinheld
worker_class = "egg:meinheld#gunicorn_worker"

# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
daemon = True

# 进程名称 -n STRING, --name STRING
# If not set, the default_proc_name setting will be used.
# default_proc_name
# pip install setproctitle
proc_name = "django:10086"

# 进程pid记录文件
# If not set, no PID file will be written.
# pidfile = os.path.join(BASE_DIR, 'log', 'web.pid')
# pidfile = "/home/log/httpd/gunweb.pid"

# logfile = os.path.join(BASE_DIR, 'log', 'debug.log')
# logfile = "/home/log/httpd/gun.log"

# 要写入的访问日志目录
accesslog = os.path.join(BASE_DIR, 'log', 'access.log')
# 要写入错误日志的文件目录。
errorlog = os.path.join(BASE_DIR, 'log', 'error.log')

# 日志格式， 使用默认
# access_log_format = '%(h)s %(t)s %(U)s %(q)s'
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 默认格式
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

#  日志等级
loglevel = 'info'
loglevel = 'debug'

# --user=apache --group=apache
# user = "apache"
# group = "apache"
