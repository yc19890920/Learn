# -*- coding:utf-8 -*-
#
import tornado.web
import tornado.httpclient
import tornado.gen

# 同步方式
class SyncHandler(tornado.web.RequestHandler):

    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.HTTPClient()
        r = client.fetch(url)
        self.write(r.body)

# 异步方式 无回调函数
class AsyncIndexHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.AsyncHTTPClient()
        r = yield tornado.gen.Task(client.fetch, url)
        self.write(r.body)
        self.finish()

# 异步方式，回调函数
class AsyncIndexHandler2(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch(url, callback=self.on_response)

    def on_response(self, response):
        self.write(response.body)
        self.finish()

