# -*- coding: utf-8 -*-

import os
from tornado.options import define

# 任务调度脚本
dirs, filename = os.path.split(os.path.abspath(__file__))
schedule_script_file = os.path.join(dirs, 'lib/' 'schedule.py')
define("SCHEDULE_SCRIPT_FILE", default=schedule_script_file)

check_email_script_file = os.path.join(dirs, 'lib/' 'check_email.py')
define("CHECK_EMAIL_SCRIPT_FILE", default=check_email_script_file)

# WEB服务器配置
# define("WEB_SERVER_IP", default="202.103.191.61")
define("WEB_SERVER_IP", default="0.0.0.0")
define("PORT", default="8888")

# 用户名密码
define("USERNAME", default="aaa")
define("PASSWORD", default="aaa")


#Redis
define("REDIS_DB_HOST", default="localhost")
define("REDIS_DB_PORT", default=6377)
define("REDIS_DB_NAME", default=0)


#接收邮件地址
define("MAIL_HOST", default="mail2.comingchina.com")
define("MAIL_ADDRESS", default="admin@comingchina.com")
define("MAIL_PASSWORD", default="girlplus1?")


