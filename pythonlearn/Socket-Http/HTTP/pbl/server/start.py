#!/usr/bin/python
#coding=utf8
import shlex
import redis
import tornadoredis
import tornado
import sys
import time
from lib.task import Task, get_ip_list_from_net
from lib.customer import Customer
from tornado.process import Subprocess
from config import *
from tornado.options import options
from tornado import web, gen
from raven.contrib.tornado import AsyncSentryClient


__author__ = 'leo'


class BaseHandler(web.RequestHandler):

    def get_login_url(self):
        return u"/login"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None


class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.html", next=self.get_argument("next", "/"))

    def post(self):
        username = self.get_argument("username", "")
        password = self.get_argument("password", "")
        # The authenticate method should match a username and password
        # to a username and password hash in the database users table.
        # Implementation left as an exercise for the reader.
        # auth = self.db.authenticate(username, password)
        if username == options.USERNAME and password == options.PASSWORD:
            auth = True
        else:
            auth = False
        if auth:
            self.set_current_user(username)
            self.redirect(self.get_argument("next", u"/"))
        else:
            error_msg = u"?error=" + tornado.escape.url_escape("Login incorrect.")
            self.redirect(u"/login" + error_msg)

    def set_current_user(self, user):
        if user:
            self.set_secure_cookie("user", tornado.escape.json_encode(user))
        else:
            self.clear_cookie("user")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        self.redirect(u"/login")


class MainHandler(BaseHandler):

    # @tornado.web.authenticated
    def get(self):
        self.redirect(u"/report")
        # self.render('index.html')


class IpManagerHandler(BaseHandler):
    @tornado.web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):
        name = self.get_argument('name', '')
        customer = Customer(self)
        ip_list = yield gen.Task(customer.get_ips, name)
        self.render('ips.html', ip_list=ip_list)

    @tornado.web.authenticated
    @web.asynchronous
    @gen.coroutine
    def post(self):

        action = self.get_argument('action', '')
        if action == 'delete':
            name = self.get_argument('name', '')
            ip = self.get_argument('ip', '')
            customer = Customer(self)
            yield gen.Task(customer.delete_ip, name, ip)

        else:
            name = self.get_argument('name', '')
            ip_list = self.get_argument('ips').split()
            customer = Customer(self)
            yield gen.Task(customer.add_ips, name, ip_list)

        self.redirect('/customer')


class CustomerDetailHandler(BaseHandler):
    @tornado.web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self, name):
        customer = Customer(self)
        data_list = yield gen.Task(customer.get_ips, name)
        self.render('customer.html', data_list=data_list)


class CustomerManagerHandler(BaseHandler):
    @tornado.web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):
        customer = Customer(self)
        data_list = yield gen.Task(customer.get_ips)
        if self.get_argument('a', 'list') == 'add':
            self.render('addcustomer.html', data_list=data_list)
        else:
            self.render('customer.html', data_list=data_list)

    @tornado.web.authenticated
    @web.asynchronous
    @gen.coroutine
    def post(self):
        action_dict = {'create': self.create(), 'put': self.put(), 'delete': self.delete()}

        action = self.get_argument('action')

        if action not in action_dict.keys():
            self.write(u'非法请求')
            self.finish()
            return
        else:
            return action_dict[action]

    @tornado.web.authenticated
    def create(self):
        name = self.get_argument('name', '')
        if not name:
            self.write(u'名称不能为空')
            self.finish()
        else:
            customer = Customer(self)
            res = yield gen.Task(customer.add_customer, name)
            if res:
                self.redirect('/customer?a=add')
            else:
                self.redirect('/customer?a=add')

    @tornado.web.authenticated
    def put(self):
        name = self.get_argument('name', '')
        new_name = self.get_argument('new_name', '')
        if (not new_name) or (not name):
            self.write(u'名称不能为空')
            self.finish()
        else:
            customer = Customer(self)
            yield gen.Task(customer.rename_customer, name, new_name)
            self.redirect('/customer')

    @tornado.web.authenticated
    def delete(self):
        name = self.get_argument('name', '')
        if not name:
            self.write(u'名称不能为空')
            self.finish()
        else:
            customer = Customer(self)
            yield gen.Task(customer.delete_customer, name)
            self.redirect('/customer')


class UmailHandler(BaseHandler):
    @tornado.web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):
        task = Task(self)
        data_dict = yield gen.Task(task.get_umail_ips)
        self.render('umail.html', data_dict=data_dict)


class TaskHandler(web.RequestHandler):
    """
    任务请求, 及导入
    """
    @web.asynchronous
    @gen.coroutine
    def get(self):
        task = Task(self)
        ip = yield gen.Task(task.get_task)
        if ip:
            self.write(ip)
            self.finish()
        else:
            self.send_error(404)


class TaskDetailHandler(web.RequestHandler):
    """
    具体任务逻辑处理
    """
    @web.asynchronous
    @gen.coroutine
    def get(self, ip):
        """
        查看任务状态
        """
        task = Task(self)
        yield task.get_task_detail(ip)
        self.write('OK')
        self.finish()

    @web.asynchronous
    @gen.coroutine
    def put(self, ip):
        """
        修改任务状态
        """
        info = self.get_argument('info', '')
        status = self.get_argument('status', '')
        if status not in ['checked', 'finished']:
            self.write("status Failed")
            self.finish()
        elif status == 'checked':
            info_list = info.split(',')
            info_dict = {'PBL': info_list[0], 'SBL': info_list[1], 'XBL': info_list[2]}
            task = Task(self)
            yield task.change_task_status(ip, status, info_dict)
            self.write("OK")
            self.finish()
        else:
            task = Task(self)
            yield task.change_task_status(ip, status, {'info': info})
            self.write("OK")
            self.finish()


class CheckHandler(web.RequestHandler):
    """
    任务请求, 及导入
    """
    @web.asynchronous
    @gen.coroutine
    def get(self):
        task = Task(self)
        ip = yield gen.Task(task.get_check)
        if ip:
            self.write(ip)
            self.finish()
        else:
            self.send_error(404)


class CheckDetailHandler(web.RequestHandler):
    """
    具体任务逻辑处理
    """
    @web.asynchronous
    @gen.coroutine
    def put(self, ip):
        """
        判断检测结果，需要处理的IP 则放入task队列
        """
        info = self.get_argument('info', '')
        status = self.get_argument('status', '')
        if status not in ['checked']:
            self.write("status Failed")
            self.finish()
        else:
            if info.find('True') > -1:
                task = Task(self)
                yield task.add_task(ip)
            self.write("OK")
            self.finish()


class BlackListHandler(web.RequestHandler):
    """
    获取黑名单记录
    """
    @web.asynchronous
    @gen.coroutine
    def get(self):
        task = Task(self)
        data_dict = yield gen.Task(task.get_blocklist)
        self.write(data_dict)
        self.finish()


class ReportHandler(BaseHandler):

    @tornado.web.authenticated
    @web.asynchronous
    @gen.coroutine
    def get(self):
        task = Task(self)
        data_dict = yield gen.Task(task.get_report)
        self.render('report.html', data_dict=data_dict)

    @web.asynchronous
    @gen.coroutine
    def post(self):
        info = self.get_argument('info', '')
        task = Task(self)
        yield task.receive_report({'info': info})
        self.write('OK')
        self.finish()


def schedule(ioloop):
    """
    任务调度
    """
    def start_interval(code):
        print "task schedule finished, code: %s" % code
        ioloop.add_timeout(time.time() + 60 * 60 * 6, lambda: schedule(ioloop))

    cmd = u"""%s %s --REDIS_DB_HOST=%s --REDIS_DB_PORT=%s --REDIS_DB_NAME=%s""" % (sys.executable,
                                                                                   options.SCHEDULE_SCRIPT_FILE,
                                                                                   options.REDIS_DB_HOST,
                                                                                   options.REDIS_DB_PORT,
                                                                                   options.REDIS_DB_NAME)

    args = shlex.split(cmd.encode('utf8'))
    print args
    Subprocess(args).set_exit_callback(start_interval)


def email_check(ioloop):
    """
    接收邮件，访问确认链接
    """
    def start_interval(code):
        print "email check , code: %s" % code
        ioloop.add_timeout(time.time() + 60*10, lambda: email_check(ioloop))

    cmd = u"""%s %s --MAIL_HOST=%s --MAIL_ADDRESS=%s --MAIL_PASSWORD=%s --REDIS_DB_HOST=%s --REDIS_DB_PORT=%s \
    --REDIS_DB_NAME=%s --WEB_SERVER_IP=%s --PORT=%s""" % (sys.executable, options.CHECK_EMAIL_SCRIPT_FILE, 
                                                          options.MAIL_HOST, options.MAIL_ADDRESS, options.MAIL_PASSWORD, 
                                                          options.REDIS_DB_HOST, options.REDIS_DB_PORT, options.REDIS_DB_NAME,
                                                          options.WEB_SERVER_IP, options.PORT)

    args = shlex.split(cmd.encode('utf8'))
    Subprocess(args).set_exit_callback(start_interval)


def initialize():
    args = sys.argv[1:]

    if 'init' in args:

        reserve_keys = ['customer', 'U-mail']

        pool = redis.ConnectionPool(host=options['REDIS_DB_HOST'], port=options['REDIS_DB_PORT'])
        r = redis.Redis(connection_pool=pool)
        name_list = r.smembers('customer')
        for name in name_list:
            reserve_keys.append((u'c_%s' % name.decode('utf8')).encode('utf8'))
        # 清除其他key
        [r.delete(k) for k in r.keys() if k not in reserve_keys]

        # 添加公司IP到任务队列
        ips = r.lrange('U-mail',0,-1)
        for ip in ips:
            hosts_list = get_ip_list_from_net(ip)
            for each in hosts_list:
                r.lpush('task', each)

        # 将现有客户所有IP都加到任务队列
        customer_list = r.lrange('customer',0,-1)
        for customer in customer_list:
            ips = r.smembers(u'c_%s' % customer.decode('utf8'))
            for ip in ips:
                hosts_list = get_ip_list_from_net(ip)
                for each in hosts_list:
                    r.lpush('task', each)

        # 关闭连接
        # pool.disconnect()


def main():
    app = tornado.web.Application(
        [
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler),
            (r"/", MainHandler),
            (r"/blacklist", BlackListHandler),
            (r"/customer", CustomerManagerHandler),
            (r"/customer/(.*)", CustomerDetailHandler),
            (r"/ips", IpManagerHandler),
            (r"/ips/umail", UmailHandler),
            (r"/report", ReportHandler),
            (r"/task", TaskHandler),
            (r"/task/([0-9\.]{7,15})", TaskDetailHandler),
            (r"/check", CheckHandler),
            (r"/check/([0-9\.]{7,15})", CheckDetailHandler),
        ],

        CONNECTION_POOL=tornadoredis.ConnectionPool(host=options['REDIS_DB_HOST'], port=options['REDIS_DB_PORT'],
                                                    max_connections=100, wait_for_available=True),

        cookie_secret="$1$uDOOIHw4$112sF6/JLaN6FYyAy6DmQ0",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=False,
        debug=True)

    app.sentry_client = AsyncSentryClient(
        'http://1e04189a9e504d8cb6b124b9224dc50c:d150ce32dc764fb0bffe3b7569e0429c@202.103.191.86:9000/2'
    )

    app.listen(options.PORT, options.WEB_SERVER_IP)
    ioloop = tornado.ioloop.IOLoop.instance()

    #初始化数据库(注:保留客户列表和客户ips)
    initialize()

    # 接收邮件确认链接
    email_check(ioloop)

    # 调度任务
    schedule(ioloop)

    ioloop.start()


if __name__ == "__main__":
    main()
