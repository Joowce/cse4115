import socketserver
import threading

from manager.userManager import UserManager

HOST = 'localhost' #Ip Blockchain server로 진행할 IP
PORT = 9009
lock = threading.Lock()


class MyTcpHandler(socketserver.BaseRequestHandler):
    userman = UserManager()

    def handle(self):
        print('[%s] is connected' % self.client_address[0])
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

        print('[%s] Termination' % self.client_address[0])
        self.userman.remove_user(username)

    def register_username(self):
        while True:
            self.request.send('role:'.encode())
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.userman.add_user(username, self.request, self.client_address):
                return username


class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def run_server():
    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        server.server_close()


run_server()
