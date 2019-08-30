import time
import os.path
import asyncio
import logging
import argparse
import websockets
from collections import deque
from urllib.parse import urlparse, parse_qs
from ansi2html import Ansi2HTMLConverter

NUM_LINES = 1000
HEARTBEAT_INTERVAL = 15 # seconds

# init
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
allowed_prefixes = []
conv = Ansi2HTMLConverter(inline=True)

@asyncio.coroutine
def view_log(websocket, path):

    logging.info('Connected, remote={}, path={}'.format(websocket.remote_address, path))

    try:
        try:
            parse_result = urlparse(path)
        except Exception:
            raise ValueError('Fail to parse URL')

        file_path = os.path.abspath(parse_result.path)
        logging.info(file_path)
        allowed = False
        for prefix in allowed_prefixes:
            if file_path.startswith(prefix):
                allowed = True
                break
        if not allowed:
            raise ValueError('Forbidden')

        if not os.path.isfile(file_path):
            raise ValueError('Not found')

        query = parse_qs(parse_result.query)
        logging.info(query)
        tail = query and query['tail'] and query['tail'][0] == '1'

        with open(file_path) as f:

            content = ''.join(deque(f, NUM_LINES))
            content = conv.convert(content, full=False)
            yield from websocket.send(content)

            if tail:
                last_heartbeat = time.time()
                while True:
                    content = f.read()
                    if content:
                        content = conv.convert(content, full=False)
                        yield from websocket.send(content)
                    else:
                        yield from asyncio.sleep(1)

                    # heartbeat
                    if time.time() - last_heartbeat > HEARTBEAT_INTERVAL:
                        try:
                            yield from websocket.send('ping')
                            pong = yield from asyncio.wait_for(websocket.recv(), 5)
                            if pong != 'pong':
                                raise Exception()
                        except Exception:
                            raise Exception('Ping error')
                        else:
                            last_heartbeat = time.time()

            else:
                yield from websocket.close()

    except ValueError as e:
        try:
            yield from websocket.send('<font color="red"><strong>{}</strong></font>'.format(e))
            yield from websocket.close()
        except Exception:
            pass

        log_close(websocket, path, e)

    except Exception as e:
        log_close(websocket, path, e)

    else:
        log_close(websocket, path)

def log_close(websocket, path, exception=None):
    message = 'Closed, remote={}, path={}'.format(websocket.remote_address, path)
    if exception is not None:
        message += ', exception={}'.format(exception)
    logging.info(message)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--prefix', required=True, action='append', help='Allowed directories')
    args = parser.parse_args()

    allowed_prefixes.extend(args.prefix)
    start_server = websockets.serve(view_log, args.host, args.port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()