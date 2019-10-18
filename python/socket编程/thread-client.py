# -*- coding: utf-8 -*-

import socket

if __name__ == '__main__':
    ports = [10002, 10003, 10004]
    for port in ports:
        address = ('localhost', port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        poem = ''
        while True:
            data = sock.recv(1024)
            if not data:
                sock.close()
                break
            poem += data
        print poem
        print "===================================="