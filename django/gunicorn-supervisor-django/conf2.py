# -*-coding:utf-8 -*-

__author__ = "YC"

import os
import multiprocessing

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 加载应用程序之前将chdir目录指定到指定目录
# gunicorn要切换到的目的工作目录
chdir = BASE_DIR

# 监听本机的5000端口
# 绑定运行的主机加端口 -b  --bind
bind = '0.0.0.0:6060'

# 开启进程
# 用于处理工作进程的数量，整数，默认为1  -w  --workers
# workers=4
workers = multiprocessing.cpu_count() * 2 + 1

# 处理请求的工作线程数，使用指定数量的线程运行每个worker。为正整数，默认为1 --threads INT
# 每个进程的开启线程
threads = multiprocessing.cpu_count() * 2

# 要使用的工作模式，默认为sync异步，类型：sync, eventlet, gevent, tornado, gthread, gaiohttp    -k STRTING, --worker-class STRTING
# 工作模式为meinheld
worker_class = "egg:meinheld#gunicorn_worker"

# 最大客户端并发数量，默认1000 --worker-connections INT
worker_connections = 2000

# 等待连接的最大数，默认2048  --backlog int
backlog = 2048

# 重新启动之前，工作将处理的最大请求数。默认值为0。
# --max-requests INT
max_requests = 0
# 要添加到max_requests的最大抖动。抖动将导致每个工作的重启被随机化，这是为了避免所有工作被重启。randint(0,max-requests-jitter)
# --max-requests-jitter INT
max_requests_jitter = 0

# 限制HTTP请求行的允许大小，默认4094。取值范围0~8190，此参数可以防止任何DDOS攻击
# --limit-request-line INT
limit_request_line = 4094
# 限制HTTP请求头字段的数量以防止DDOS攻击，与limit-request-field-size一起使用可以提高安全性。默认100，最大值32768
# --limit-request-fields INT
limit_request_fields = 100
# 限制HTTP请求中请求头的大小，默认8190。值是一个整数或者0，当该值为0时，表示将对请求头大小不做限制
# --limit-request-field-size INT
limit_request_field_size = 8190

# debug=True

# 进程名称
proc_name = os.path.join(BASE_DIR, 'gunicorn.pid') # 'gunicorn.pid'

# 设置pid文件的文件名，如果不设置将不会创建pid文件 -p FILE, --pid FILE
# 进程pid记录文件
pidfile = os.path.join(BASE_DIR, 'app.pid')
# 日志文件路径 --access-logfile FILE
logfile = os.path.join(BASE_DIR, 'debug.log') # 'debug.log'

# 日志文件路径  --access-logfile FILE
# 要写入的访问日志目录
accesslog = os.path.join(BASE_DIR, 'access.log')  # 'access.log'
# 错误日志文件路径 --error-logfile FILE, --log-file FILE
# 要写入错误日志的文件目录。
errorlog = os.path.join(BASE_DIR, 'error.log')
# 设置gunicorn访问日志格式，错误日志无法设置
# 日志格式，--access_log_format '%(h)s %(l)s %(u)s %(t)s'
access_log_format = '%(h)s %(t)s %(U)s %(q)s'
# access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
# 日志输出等级 --log-level LEVEL
loglevel = 'debug'
# loglevel = 'info'

# 在代码改变时自动重启，默认False   --reload
# 代码更新时将重启工作，默认为False。此设置用于开发，每当应用程序发生更改时，都会导致工作重新启动。
reload = False

# 选择重载的引擎，支持的有三种： auto  pull   inotity：需要下载
# --reload-engine STRTING
reload_engine = "auto"

# 如果不使用supervisord之类的进程管理工具可以是进程成为守护进程，否则会出问题
# 守护Gunicorn进程，默认False    --daemon
daemon = False

# 超过设置后工作将被杀掉并重新启动，默认30s，nginx默认60s    -t INT, --timeout INT
timeout = 30

# 默认30，在超时(从接收到重启信号开始)之后仍然活着的工作将被强行杀死；一般默认
# 优雅的人工超时时间，默认情况下，这个值为30。收到重启信号后，工作人员有那么多时间来完成服务请求。在超时(从接收到重启信号开始)之后仍然活着的工作将被强行杀死。
# --graceful-timeout INT
graceful_timeout = 30

# 在keep-alive连接上等待请求的秒数，默认情况下值为2。一般设定在1~5秒之间
# --keep-alive INT
keepalive = 2

# 打印服务器执行过的每一条语句，默认False。此选择为原子性的，即要么全部打印，要么全部不打印
# --spew
spew = False

# 显示当前的配置，默认False，即显示  --check-config
check_config = False

# 在工作进程被复制(派生)之前加载应用程序代码，默认为False。通过预加载应用程序，你可以节省RAM资源，并且加快服务器启动时间。
# --preload
preload_app = False

# 设置环境变量 -e ENV, --env ENV
# 设置环境变量(key=value)，将变量传递给执行环境，如：
# gunicorin -b 127.0.0.1:8000 -e abc=123 manager:app
# 在配置文件中写法： raw_env=["abc=123"]
raw_env = ["abc=123"]



