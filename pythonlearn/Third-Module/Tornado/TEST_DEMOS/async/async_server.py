# -*- coding:utf-8 -*-
#

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpclient
import tornado.gen

import os

from tornado.options import options, define
define("port", default="8000", type=int, help="run on the given port")

# 同步方式
class IndexHandler1(tornado.web.RequestHandler):

    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.HTTPClient()
        r = client.fetch(url)
        self.write(r.body)

# 异步方式， 回调函数
class IndexHandler2(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch(url, callback=self.on_response)

    def on_response(self, response):
        self.write(response.body)
        self.finish()

# 异步方式 无回调
class IndexHandler3(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.AsyncHTTPClient()
        r = yield tornado.gen.Task(client.fetch, url)
        self.write(r.body)
        self.finish()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    settings = {
        # "static_path":  os.path.join(os.path.dirname(__file__), "static"),
        # "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        # "login_url": "/login"
        "cookie_secret": "UqOmbxPmT5C2DdxhpL0NIkF/DhV/jkOovm9AO2s5Fy8=",
        "xsrf_cookies": True
    }
    app = tornado.web.Application([
        (r"/", IndexHandler1),
        (r"/i2", IndexHandler2),
        (r'/i3',IndexHandler3),
    ], **settings)
    server = tornado.httpserver.HTTPServer(app)
    server.bind(options.port)
    # 多进程
    # server.start(10)
    #启动Ioloop轮循监听
    # tornado.ioloop.IOLoop.current().start()

    # 单进程
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()


