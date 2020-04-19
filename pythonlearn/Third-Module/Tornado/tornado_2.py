# -*- coding:utf-8 -*-
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

class IndexHandler(RequestHandler):
    def get(self):
        self.write(u'给自己一点时间，理清所有的荒唐与期望。')

if __name__ == '__main__':
    app = Application([(r'/',IndexHandler)])
    http_server = HTTPServer(app, debug=True)
    #最原始的方式
    http_server.bind(8888)
    http_server.start(10)

    #启动Ioloop轮循监听
    IOLoop.current().start()
