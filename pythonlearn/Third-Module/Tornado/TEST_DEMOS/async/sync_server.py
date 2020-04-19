# -*- coding:utf-8 -*-
#

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time

from tornado.options import options, define
define("port", default="8000", type=int, help="run on the given port")

class IndexHandler1(tornado.web.RequestHandler):

    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.HTTPClient()
        r = client.fetch(url)
        self.write(r.body)

class IndexHandler2(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        url = "http://demo.pythoner.com/itt2zh/ch5.html"
        client = tornado.httpclient.AsyncHTTPClient()
        client.fetch(url, callback=self.on_response)

    def on_response(self, response):
        self.write(response.body)
        self.finish()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
        (r"/i1", IndexHandler1),
        (r"/i2", IndexHandler2)
    ])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()