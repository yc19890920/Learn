# -*- coding: utf-8 -*-
import logging
import json
from websocket_server import WebsocketServer
import sys

# 因为考虑到传入的字符串有非英文字符，
# 所以手动设置编码，否则可能会报编码错误
reload(sys)
sys.setdefaultencoding('utf-8')

def new_client(client, server):
    print client
    print("Client(%d) has joined." % client['id'])


def client_left(client, server):
    print("Client(%d) disconnected" % client['id'])


def message_back(client, server, message):
    print "=================", type(message)
    _message = json.loads(message)
    print "=================", type(_message), _message
    # 这里的message参数就是客户端传进来的内容
    print("Client(%d) said: %s" % (client['id'], message))
    # 这里可以对message进行各种处理
    result = "服务器已经收到消息了..." + message
    # 将处理后的数据再返回给客户端
    server.send_message(client, result)


# 新建一个WebsocketServer对象，第一个参数是端口号，第二个参数是host
# 如果host为空，则默认为本机IP
server = WebsocketServer(4200, host='localhost')
# 设置当有新客户端接入时的动作
server.set_fn_new_client(new_client)
# 设置当有客户端断开时的动作
server.set_fn_client_left(client_left)
# 设置当接收到某个客户端发送的消息后的操作
server.set_fn_message_received(message_back)
# 设置服务一直运行
server.run_forever()


