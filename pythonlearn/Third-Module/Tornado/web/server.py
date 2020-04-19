# -*- coding:utf-8 -*-
#
import sys
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import options

from application import app

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    print>>sys.stderr, "Development server is running at http://127.0.0.1:%s" % options.port
    print>>sys.stderr, "Quit the server with Control-C"
    # print "Development server is running at http://127.0.0.1:%s" % options.port
    # print "Quit the server with Control-C"
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()