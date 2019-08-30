# -*- coding: UTF-8 -*-
import gevent.monkey
gevent.monkey.patch_all()
import os
import sys
import pwd
import signal
import time
import socket
import logging
import asyncore

class EchoClient(asyncore.dispatcher):
    """Sends messages to the server and receives responses.
    """

    def __init__(self, host, port, message, chunk_size=512):
        self.message = message
        self.to_send = message
        self.received_data = []
        self.chunk_size = chunk_size
        self.logger = logging.getLogger('EchoClient')
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.debug('connecting to %s', (host, port))
        self.connect((host, port))
        return

    def handle_connect(self):
        self.logger.debug('handle_connect()')

    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()
        received_message = ''.join(self.received_data)
        if received_message == self.message:
            self.logger.debug('RECEIVED COPY OF MESSAGE')
        else:
            self.logger.debug('ERROR IN TRANSMISSION')
            self.logger.debug('EXPECTED "%s"', self.message)
            self.logger.debug('RECEIVED "%s"', received_message)
        return

    def writable(self):
        self.logger.debug('writable() -> %s', bool(self.to_send))
        return bool(self.to_send)

    def handle_write(self):
        sent = self.send(self.to_send[:self.chunk_size])
        self.logger.debug('handle_write() -> (%d) "%s"', sent, self.to_send[:sent])
        self.to_send = self.to_send[sent:]

    def handle_read(self):
        data = self.recv(self.chunk_size)
        self.logger.debug('handle_read() -> (%d) "%s"', len(data), data)
        self.received_data.append(data)

def handle_exit(*args, **kw):
    logging.info('emstpd(pid=%s) exited', os.getpid())
    sys.exit()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        # format='%(name)s: %(message)s',
                        format='%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s',
                        )

    client = EchoClient('localhost', 33333, message=open('requirement.txt', 'r').read())

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass