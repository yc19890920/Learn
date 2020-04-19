# -*- coding:utf-8 -*-
#

import tornado.web

class BaseHandler(tornado.web.RequestHandler):

    def get_login_url(self):
        return u"/"

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return tornado.escape.json_decode(user_json)
        else:
            return None

    def clear_auth_cookie(self):
        self.clear_cookie("user")

    @property
    def db(self):
        return self.application.db



__all__ = ["BaseHandler"]