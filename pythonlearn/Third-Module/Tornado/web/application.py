# -*- coding:utf-8 -*-
#

import os
import torndb
import tornadoredis
import tornado.web
from urls import URLS
from conf import settings

from tornado.options import define, options
define("port", default=8888, help="run port", type=int)

# MySQL
define("mysql_host", default="{}:{}".format(settings.DATABASES["default"]["HOST"], settings.DATABASES["default"]["PORT"]), help="db host")
define("mysql_database", default=settings.DATABASES["default"]["NAME"], help="db name")
define("mysql_user", default=settings.DATABASES["default"]["USER"], help="db user")
define("mysql_password", default=settings.DATABASES["default"]["PASSWORD"], help="db password")

# Redis
define("REDIS_DB_HOST", default=settings.REDIS_CACHES["HOST"])
define("REDIS_DB_PORT", default=settings.REDIS_CACHES["PORT"])
define("REDIS_DB_NAME", default=settings.REDIS_CACHES["NAME"])

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "template")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = URLS
        settings = dict(
            login_url="/",
            # 服务器进程将会重新启动, 文件改变
            # autoreload=True,
            # 设置成调试模式
            # debug=True,
            xsrf_cookies=True,
            # xheaders=True,
            # 设定 cookie_secret, 用于 secure_cookie
            cookie_secret="UqOmbxPmT5C2DdxhpL0NIkF/DhV/jkOovm9AO2s5Fy8=",
            # 设定 session_secret 用于生成 session_id
            template_path = TEMPLATE_PATH,
            static_path = STATIC_PATH,
            CONNECTION_POOL=tornadoredis.ConnectionPool(
                host=options.REDIS_DB_HOST, port=options.REDIS_DB_PORT,
                max_connections=100, wait_for_available=True),
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = torndb.Connection(
            host = options.mysql_host,
            database = options.mysql_database,
            user = options.mysql_user,
            password = options.mysql_password
        )

app = Application()