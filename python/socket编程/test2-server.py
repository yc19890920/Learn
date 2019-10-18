# -*- coding:utf-8 -*-

import socket
import traceback
import json

HOST = "localhost"
PORT = 10002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

while 1:
    conn, addr = s.accept()
    print u'connect %s!' % (addr,)
    while 1:
        try:
            msg = conn.recv(1024)
            if not msg:
                break

            print msg.decode("utf-8"), type(msg.decode("utf-8"))
            if msg == 'quit':
                conn.send( json.dumps({
                    "msg": msg.decode("utf-8"),
                    "quit": True,
                }) )
                break

            # 将收到的消息回发回去
            conn.send( json.dumps({
                "msg": msg.decode("utf-8"),
                "quit": False,
            }) )
        except BaseException as e:
            print traceback.format_exc()
            break
    print "==============close conn"
    conn.close()

s.close()
