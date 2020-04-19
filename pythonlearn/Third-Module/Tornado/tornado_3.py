# -*- coding:utf-8 -*-

from tornado.web import Application, RequestHandler, url
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer


class IndexHandler(RequestHandler):

    def get(self):
        self.write("<a href='"+self.reverse_url("login")+"'>用户登录</a>")


class RegistHandler(RequestHandler):
    def initialize(self, title):
        self.title = title

    def get(self):
        self.write("注册业务处理:" + str(self.title))


class LoginHandler(RequestHandler):
    def get(self):
        self.write("用户登录页面展示")

    def post(self):
        self.write("用户登录功能处理")


if __name__ == "__main__":
    app = Application(
        [
            (r"/", IndexHandler),
            (r"/regist", RegistHandler, {"title": "会员注册"}),
            url(r"/login", LoginHandler, name="login"),
        ]
    )

    http_server = HTTPServer(app)
    http_server.listen(8000)

    IOLoop.current().start()