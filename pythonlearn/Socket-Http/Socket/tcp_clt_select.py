# -*- coding: utf-8 -*-
#
import datetime, errno, optparse, select, socket

def connect(port):
    """Connect to the given server and return a non-blocking socket."""
    address = (str('127.0.0.1'), port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.setblocking(0)
    return sock

def format_address(address):
    host, port = address
    return '%s:%s' % (host or '127.0.0.1', port)

if __name__ == '__main__':
    ports = [10010, 10011, 10012]
    start = datetime.datetime.now()

    sockets = map(connect, ports)
    poems = dict.fromkeys(sockets, '') # socket -> accumulated poem
    print poems

    # socket -> task numbers
    sock2task = dict([(s, i + 1) for i, s in enumerate(sockets)])
    sockets = list(sockets) # make a copy
    print sockets
    while sockets:
        #运用select来确保那些可读取的异步socket可以立即开始读取IO
        #OS不停的搜索目前可以read的socket，有的话就返回rlist
        rlist, _, _ = select.select(sockets, [], [])
        for sock in rlist:
            data = ''
            while True:
                try:
                    new_data = sock.recv(1024)
                except socket.error, e:
                    if e.args[0] == errno.EWOULDBLOCK:
                        break
                    raise
                else:
                    if not new_data:
                        break
                    else:
                        print new_data
                        data += new_data

            task_num = sock2task[sock]
            if not data:
                sockets.remove(sock)
                sock.close()
                print 'Task %d finished' % task_num
            else:
                addr_fmt = format_address(sock.getpeername())
                msg = 'Task %d: got %d bytes of poetry from %s'
                print  msg % (task_num, len(data), addr_fmt)

            poems[sock] += data

    elapsed = datetime.datetime.now() - start
    print 'Got poems in %s' %  elapsed