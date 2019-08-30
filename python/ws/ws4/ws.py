# -*- coding: utf-8 -*-
import redis
from flask import Flask, request, render_template, abort
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

redis = redis.Redis()
key = "aaaaaaaaaaaaaa"
# 消息KEY
app = Flask(__name__)

@app.route('/ws')
def echo():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        if ws is None:
            abort(404)
        else:
            while True:
                if not ws.closed:
                    # message = ws.receive()
                    ls = redis.brpop(key, timeout=5)
                    if not ls: continue
                    print "===================", ls
                    ws.send(ls[1])
                else:
                    ws.close()


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8765), app, handler_class=WebSocketHandler)
    http_server.serve_forever()