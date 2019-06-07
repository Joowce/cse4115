import threading
import logging

lock = threading.Lock()


class UserManager:

    def __init__(self):
        self.users = {}

    def add_user(self, username, conn, addr):
        if username in self.users:
            conn.send('already registered \n'.encode())
            return None

        lock.acquire()
        self.users[username] = (conn, addr)
        lock.release()

        self.send_message_to_all('[%s] user \'%s\' is join.' % addr % username)
        logging.info('+++ Number of Participation [%d]' % len(self.users))

        return username

    def remove_user(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.send_message_to_all('[%s] is quit.' % username)
        logging.info('--- Number of Participation [%d]' % len(self.users))

    def send_message_to_all(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())