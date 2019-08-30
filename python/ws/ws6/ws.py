import json
import random
from gevent import pywsgi, sleep
from geventwebsocket.handler import WebSocketHandler


class WebSocketApp(object):
    def __call__(self, env, start_response):
        ws = env['wsgi.websocket']
        print dir(ws), id(ws)
        # ['OPCODE_BINARY', 'OPCODE_CLOSE', 'OPCODE_CONTINUATION', 'OPCODE_PING', 'OPCODE_PONG', 'OPCODE_TEXT',
        #  '__class__', '__del__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__',
        #  '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__',
        #  '__str__', '__subclasshook__', '_decode_bytes', '_encode_bytes', '_is_valid_close_code', 'close', 'closed',
        #  'current_app', 'environ', 'handle_close', 'handle_ping', 'handle_pong', 'handler', 'logger', 'origin', 'path',
        #  'protocol', 'raw_read', 'raw_write', 'read_frame', 'read_message', 'receive', 'send', 'send_frame', 'stream',
        #  'utf8validate_last', 'utf8validator', 'validate_utf8', 'version']

        x = 0
        while True:
            data = json.dumps({'x': x, 'y': random.randint(1, 5)})
            ws.send(data)
            x += 1
            sleep(0.5)


server = pywsgi.WSGIServer(('0.0.0.0', 10000), WebSocketApp(), handler_class=WebSocketHandler)
server.serve_forever()