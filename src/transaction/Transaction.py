import time
import json


class Transaction(object):
    def __init__(self, sender=None, receiver=None, message=None):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.tx_id = "B" + self.timestamp
        self.message = message
        self.signature = ''

    def load_dict(self, total_dict):
        self.sender = total_dict.get('sender')
        self.receiver = total_dict.get('receiver')
        self.timestamp = total_dict.get('timestamp')
        self.tx_id = total_dict.get('tx_id')
        self.message = total_dict.get('message')
        self.signature = total_dict.get('signature')
        return self

    def get_data(self):
        data = vars(self).copy()
        del(data['signature'])
        return json.dumps(data)

    def add_signature(self, signature):
        self.signature = signature


if __name__ == '__main__':
    t = Transaction('test', 'test', 'test')
    print(t.get_data())

