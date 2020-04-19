# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.options
import tornado.web
import tornado.ioloop

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

#定义处理类型
class IndexHandler(tornado.web.RequestHandler):
    #添加一个处理get请求方式的方法
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')
        #向响应中，添加数据
        self.write(greeting + ', friendly user!')

if __name__ == '__main__':

    tornado.options.parse_command_line()
    #创建一个应用对象
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    #绑定一个监听端口
    http_server.listen(options.port)
    #启动web程序，开始监听端口的连接
    tornado.ioloop.IOLoop.instance().start()