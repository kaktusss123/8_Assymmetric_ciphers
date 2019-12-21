from socket import socket
from pickle import dumps, loads
from random import randint

def send(sock, msg):
    msg = msg.encode()
    header = f'{len(msg):10}'.encode()
    sock.send(header + msg)

def recv(sock):
    header = sock.recv(10)
    header = int(header.decode())
    msg = sock.recv(header)
    return msg.decode()

def auth(sock):
    A, g, p = loads(sock.recv(1024))
    b = randint(100, 100000)
    B = g ** b % p
    sock.send(dumps(B))
    K = A ** b % p
    return K


if __name__ == '__main__':
    sock = socket()
    try:
        sock.bind(('', 8080))
    except OSError:
        sock.bind(('', 0))
    finally:
        with open('port', 'w') as f:
            f.write(str(sock.getsockname()[1]))

    sock.listen(1)
    try:
        while 1:
            conn, addr = sock.accept()
            key = auth(conn)
            print(f'Server key: {key}')
            conn.close()
    finally:
        sock.close()