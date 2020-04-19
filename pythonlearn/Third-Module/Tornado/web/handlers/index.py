# -*- coding:utf-8 -*-
#

import tornado.web
import tornado.gen

from lib import DB
from handlers import BaseHandler


class LoginHandler(BaseHandler):

    error_message = {
        '100': u'信息填写不完整',
        '101': u'该用户不存在',
        '102': u'密码错误',
        '103': u'验证码错误',
    }

    def get(self):
        self.render("login.html", error=None)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        if not username or not password:
            self.render("login.html", error=100)
            return
        user_infos = yield tornado.gen.Task(DB.query_user, self.db, username)
        if user_infos:
            if self.check_password(password, user_infos[0]["password"]):
                self.set_current_user(username, )
                self.redirect("/user")
            else:
                self.render("login.html", error=102)
                return
        else:
            self.render("login.html", error=101)
            return

    @staticmethod
    def check_password(raw_password, md5_password=None):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        from passlib.hash import md5_crypt
        return md5_crypt.verify(raw_password, md5_password)

    def set_current_user(self, user):
        if user:
            #注意这里使用了 tornado.escape.json_encode() 方法
            self.set_secure_cookie('user', tornado.escape.json_encode(user), expires_days=7)
        else:
            self.clear_cookie("user")

class LogoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.clear_auth_cookie()
        self.redirect('/')

# import urlparse
class UserHandler(BaseHandler):

    @tornado.web.authenticated
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        # print '--------------', self.request.uri
        # base_url = urlparse.urlsplit(self.request.uri)
        # print '--------------', base_url
        # query_args = urlparse.parse_qs(base_url.query)
        # print '--------------', query_args
        username = self.get_current_user()
        user_infos = yield tornado.gen.Task(DB.query_user, self.db, username)
        self.render("user.html", users=user_infos)

    def write_error(self, status_code, **kwargs):
        self.set_header("Content-Type", "text/plain")
        if "exc_info" in kwargs:
            self.write("Exception: %s" % kwargs["exc_info"][0].__name__)
        else:
            self.write("Status: %d" % status_code)