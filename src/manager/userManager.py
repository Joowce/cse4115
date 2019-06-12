import threading
import logging
from connection.Message import wrap_neighbor, wrap_neighbor_list, wrap_logout
lock = threading.Lock()


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, user, conn, addr):
        if user.name in self.users:
            conn.send('already registered \n'.encode())
            return None

        user.conn = conn
        user.addr = addr

        message = wrap_neighbor(user)
        self.send_message_to_all(message)

        lock.acquire()
        self.users[user.name] = user
        lock.release()

        conn.send(wrap_neighbor_list(self.users.values()).encode())
        logging.info('+++ Number of Participation [%d]' % len(self.users))

        return user.name

    def remove_user(self, username):
        if username not in self.users:
            return

        user = self.users[username]

        lock.acquire()
        del(self.users[username])
        lock.release()

        self.send_message_to_all(wrap_logout(user))

        logging.info('--- Number of Participation [%d]' % len(self.users))

    def send_message_to_all(self, msg):
        for user in self.users.values():
            conn = user.conn
            conn.send(msg.encode())

    def message_handler(self, username, msg):
        if msg == 'logout':
            logging.info('[%s] user request logout' % username)
            return -1

        self.send_message_to_all(msg)
        return 1
