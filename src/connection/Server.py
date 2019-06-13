import socketserver
import threading
from connection.Message import parse_message
from manager.userManager import UserManager
import logging
import sys, getopt


HOST = 'localhost' #Ip Blockchain server로 진행할 IP
PORT = 9009
lock = threading.Lock()


class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):
        logging.info('%s is connected' % str(self.client_address))
        username = ''
        try:
            username = self.register_user()
            msg = self.request.recv(1024)
            while msg:
                logging.info('%s: %s' % (str(self.client_address), msg))
                if self.userman.message_handler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(10240)

        except Exception as e:
            print(e)

        logging.info('%s Termination' % str(self.client_address))
        self.userman.remove_user(username)

    def register_user(self):
        while True:
            message = self.request.recv(10240)
            message = message.decode()
            msg_type, user = parse_message(message)
            username = self.userman.add_user(user, self.request, self.client_address)
            if username:
                return username


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def run_server():
    server = None
    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "l", ["log="])

    for opt, arg in opts:
        if opt in ("-l", "--log"):
            level = getattr(logging, arg.upper())
            logging.basicConfig(level=level)

    run_server()
