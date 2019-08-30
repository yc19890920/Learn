import gevent.monkey
gevent.monkey.patch_all()
from gevent.pool import Pool
from gevent.server import StreamServer

def handle(socket, address):
    print('new connection!')

pool = Pool(10000) # do not accept more than 10000 connections
server = StreamServer(('127.0.0.1', 1234), handle, spawn=pool)
server.serve_forever()