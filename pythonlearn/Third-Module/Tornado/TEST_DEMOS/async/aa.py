# -*- coding:utf-8 -*-
#

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options

import tornado.httpclient
import tornado.gen

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
    @tornado.gen.engine
    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.AsyncHTTPClient()
        r = yield tornado.gen.Task(client.fetch, url)
        self.write(r.body)
        self.finish()

if __name__ == '__main__':
    app = tornado.web.Application([
        (r"/i1", IndexHandler1),
        (r"/i2", IndexHandler2),
        (r'/i3',IndexHandler3),
    ])
    http_server = tornado.httpserver.HTTPServer(app)
    #最原始的方式
    http_server.bind(options.port)
    http_server.start(5)

    #启动Ioloop轮循监听
    tornado.ioloop.IOLoop.current().start()