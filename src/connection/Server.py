import socketserver
import threading
import json
from manager.userManager import UserManager


HOST = 'localhost' #Ip Blockchain server로 진행할 IP
PORT = 9009
lock = threading.Lock()


class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):
        print('%s is connected' % str(self.client_address))
        username = ''
        try:
            username = self.register_username()
            msg = self.request.recv(1024)
            while msg:
                print(msg.decode())
                if self.userman.message_handler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)

        except Exception as e:
            print(e)

        print('%s Termination' % str(self.client_address))
        self.userman.remove_user(username)

    def register_username(self):
        while True:
            user = self.request.recv(1024)
            user = user.decode()
            user = json.loads(user)
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
    run_server()
