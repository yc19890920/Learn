import gevent
import gevent.monkey
gevent.monkey.patch_all()

import pprint
import json
import traceback
import gevent.pywsgi
from geventwebsocket.handler import WebSocketHandler, Client
import logging
from geventwebsocket.logging import create_logger

_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s'))
log = logging.getLogger(__name__)
log.addHandler(_handler)
log.setLevel(logging.DEBUG)

USERS = set()
G_USERS = dict()
STATE = {"value": 0}

ws_send = lambda user, message: user.send(message)

def ws_state_event():
    x = {"type": "state"}
    x.update(STATE)
    return json.dumps(x)

def ws_users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def ws_notify_state():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = ws_state_event()
        log.error(message)
        map(lambda obj: ws_send(obj, message), USERS)

def ws_notify_users():
    if USERS:  # asyncio.wait doesn't accept an empty list
        message = ws_users_event()
        log.error(message)
        map(lambda obj: ws_send(obj, message), USERS)

def ws_register(ws):
    USERS.add(ws)
    G_USERS[ws] = ws
    ws_notify_users()

def ws_unregister(ws):
    USERS.remove(ws)
    del G_USERS[ws]
    ws.close()
    ws_notify_users()

class WebSocketApp(object):
    def __call__(self, env, start_response):
        ws = env['wsgi.websocket']
        pprint.pprint(ws.environ)
        # print "=======environ========", ws.environ
        # print "=======origin========", ws.origin
        # print "=======path========", ws.path
        # print "=======protocol========", ws.protocol
        # print "=======version========", ws.version
        # print dir(ws), id(ws)
        # ['OPCODE_BINARY', 'OPCODE_CLOSE', 'OPCODE_CONTINUATION', 'OPCODE_PING', 'OPCODE_PONG', 'OPCODE_TEXT',
        #  '__class__', '__del__', '__delattr__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__',
        #  '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__slots__',
        #  '__str__', '__subclasshook__', '_decode_bytes', '_encode_bytes', '_is_valid_close_code', 'close', 'closed',
        #  'current_app', 'environ', 'handle_close', 'handle_ping', 'handle_pong', 'handler', 'logger', 'origin', 'path',
        #  'protocol', 'raw_read', 'raw_write', 'read_frame', 'read_message', 'receive', 'send', 'send_frame', 'stream',
        #  'utf8validate_last', 'utf8validator', 'validate_utf8', 'version']
        ws_register(ws)
        try:
            ws.send(ws_state_event())
            while True:
                message = ws.receive()
                data = json.loads(message)
                if data["action"] == "minus":
                    STATE["value"] -= 1
                    ws_notify_state()
                elif data["action"] == "plus":
                    STATE["value"] += 1
                    ws_notify_state()
                else:
                    log.error("unsupported event: %s", data)
                    gevent.sleep(0.01)
        except:
            log.error(traceback.format_exc())
        finally:
            ws_unregister(ws)

class WebSocketAppHandler(WebSocketHandler):
    def run_websocket(self):
        """
        Called when a websocket has been created successfully.
        """

        if getattr(self, 'prevent_wsgi_call', False):
            return

        # In case WebSocketServer is not used
        if not hasattr(self.server, 'clients'):
            self.server.clients = {}

        # Since we're now a websocket connection, we don't care what the
        # application actually responds with for the http response

        try:
            self.server.clients[self.client_address] = Client(
                self.client_address, self.websocket)
            list(self.application(self.environ, lambda s, h, e=None: []))
        except Exception as e:
            self.logger.error(e)
            # raise e
        finally:
            del self.server.clients[self.client_address]
            if not self.websocket.closed:
                self.websocket.close()
            self.environ.update({
                'wsgi.websocket': None
            })
            self.websocket = None

    @property
    def logger(self):
        if not hasattr(self.server, 'logger'):
            self.server.logger = log
        return self.server.logger

    def upgrade_websocket(self):
        super(WebSocketAppHandler, self).upgrade_websocket()

    def upgrade_connection(self):
        super(WebSocketAppHandler, self).upgrade_connection()



def server(host="127.0.0.1", port=9999):
    ws = gevent.pywsgi.WSGIServer((host, port), WebSocketApp(), handler_class=WebSocketAppHandler)
    ws.serve_forever()

def main():
    gevent.joinall([
        gevent.spawn(server, '0.0.0.0', 10000),
        gevent.spawn(server, '0.0.0.0', 10002),
        # gevent.spawn( gevent.pywsgi.WSGIServer(('0.0.0.0', 10002), WebSocketApp(), handler_class=WebSocketHandler).serve_forever ),
        # gevent.spawn(put_routine),
    ])


if __name__ == '__main__':
    main()

# server = gevent.pywsgi.WSGIServer(('0.0.0.0', 10000), WebSocketApp(), handler_class=WebSocketHandler)
# server.serve_forever()