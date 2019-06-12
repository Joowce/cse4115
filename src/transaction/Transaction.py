import time
import json


class Transaction(object):
    def __init__(self, sender, receiver, message):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.tx_id = "B" + self.timestamp
        self.message = message
        self.signature = ''

    def get_data(self):
        data = self.__dict__
        del(data['signature'])
        return json.dumps(data)

    def add_signature(self, signature):
        self.signature = signature


if __name__ == '__main__':
    t = Transaction('test', 'test', 'test')
    print(t.get_data())

