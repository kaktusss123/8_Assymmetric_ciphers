from socket import socket
from random import randint
from pickle import dumps, loads

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
    a, g, p = (randint(100, 100000) for _ in range(3))
    A = g ** a % p
    sock.send(dumps((A, g, p)))
    B = loads(sock.recv(1024))
    K = B ** a % p
    return K

if __name__ == "__main__":
    with open('port') as f:
        port = int(f.read())
    
    sock = socket()
    sock.connect(('localhost', port))
    key = auth(sock)
    print(f'Client key: {key}')

