# -*- coding: utf-8 -*-

from SocketServer import TCPServer as TCP, StreamRequestHandler as SRH
from time import ctime

# Address and Port
HOST = ''
PORT = 10010
ADDR = (HOST, PORT)

# BuffSize
BUFSIZ = 1024

# build RequestHandler
class MyRequestHandler(SRH):
    def handle(self):
        print '...connected from: ', self.client_address
        self.wfile.write('[%s] %s' % (ctime(), self.rfile.readline()))

# build TCPServer
TCPServ = TCP(ADDR, MyRequestHandler)
print 'waiting for connection...'
# loop to process
TCPServ.serve_forever()

