# -*- coding: UTF-8 -*-
import gevent.monkey
gevent.monkey.patch_all()
import gevent
import os
import sys
import pwd
import signal
import socket
import logging
import asyncore

class EchoServer(asyncore.dispatcher):
    """Receives connections and establishes handlers for each client.
    """

    def __init__(self, address):
        self.logger = logging.getLogger('EchoServer')
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(address)
        self.address = self.socket.getsockname()
        self.logger.debug('binding to %s', self.address)
        self.listen(1)
        return

    def handle_accept(self):
        # Called when a client connects to our socket
        client_info = self.accept()
        self.logger.debug('handle_accept() -> %s', client_info[1])
        EchoHandler(sock=client_info[0])
        # We only want to deal with one client at a time,
        # so close as soon as we set up the handler.
        # Normally you would not do this and the server
        # would run forever or until it received instructions
        # to stop.
        self.handle_close()
        return

    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()
        return

class EchoHandler(asyncore.dispatcher):
    """Handles echoing messages from a single client.
    """

    def __init__(self, sock, chunk_size=256):
        self.chunk_size = chunk_size
        self.logger = logging.getLogger('EchoHandler%s' % str(sock.getsockname()))
        asyncore.dispatcher.__init__(self, sock=sock)
        self.data_to_write = []
        return

    def writable(self):
        """We want to write if we have received data."""
        response = bool(self.data_to_write)
        self.logger.debug('writable() -> %s', response)
        return response

    def handle_write(self):
        """Write as much as possible of the most recent message we have received."""
        data = self.data_to_write.pop()
        sent = self.send(data[:self.chunk_size])
        if sent < len(data):
            remaining = data[sent:]
            self.data.to_write.append(remaining)
        self.logger.debug('handle_write() -> (%d) "%s"', sent, data[:sent])
        if not self.writable():
            self.handle_close()

    def handle_read(self):
        """Read an incoming message from the client and put it into our outgoing queue."""
        data = self.recv(self.chunk_size)
        self.logger.debug('handle_read() -> (%d) "%s"', len(data), data)
        self.data_to_write.insert(0, data)

    def handle_close(self):
        self.logger.debug('handle_close()')
        self.close()

def handle_exit(*args, **kw):
    logging.info('echo(pid=%s) exited', os.getpid())
    sys.exit()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        # format='%(name)s: %(message)s',
                        format='%(asctime)s %(levelname)s %(module)s:%(lineno)s %(message)s',
                        )

    address = ('localhost', 33333) # let the kernel give us a port
    server = EchoServer(address)
    # ip, port = server.address # find out what port we were given

    if os.getuid() == 0:
        try:
            os.setuid(pwd.getpwnam('python').pw_uid)
        except KeyError as e:
            logging.error(e)
            os.setuid(99)

    for i in range(5):
        if not os.fork():
            signal.signal(signal.SIGINT, handle_exit)
            signal.signal(signal.SIGTERM, handle_exit)
            signal.signal(signal.SIGCHLD, handle_exit)
            logging.info('echo child (pid=%s) started', os.getpid())
            break

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass