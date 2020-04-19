import socket


if __name__ == '__main__':
    ports = [10010, 10011, 10012]
    for port in ports:
        address = (str('127.0.0.1'), port)
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