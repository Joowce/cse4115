import socket
from threading import Thread
import json
import logging

HOST = 'localhost'
PORT = 9009


def receive(sock, rcv_handler):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            rcv_handler(data.decode())
        except Exception as e:
            logging.error(e)


def start(user, rcv_handler, get_message):
    """
        for starting client
        :param user: dictionary
        :param rcv_handler: handler massages client received
        :param get_message: get message from control
        :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        t = Thread(target=receive, args=(sock, rcv_handler))
        t.daemon = True
        t.start()

        msg = json.dumps(user)
        sock.send(msg.encode())

        while True:
            msg = get_message()
            msg = json.dumps(msg)
            sock.send(msg.encode())


if __name__ == "__main__":
    start({'name': 'test'}, print, input)
