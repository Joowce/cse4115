import socket
import logging

HOST = 'localhost'
PORT = 9009
MAX_SIZE = 1024
logging.basicConfig(level=logging.INFO)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Client:
    def __init__(self):
        sock.connect((HOST, PORT))
        self.sock = sock
        logging.info('server connected')

    def receive(self):
        data = self.sock.recv(MAX_SIZE)
        return data.decode()

    def send(self, message):
        return self.sock.send(message.encode())

    def __exit__(self):
        self.sock.close()