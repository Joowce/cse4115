import time


class Transaction(object):
    def __init__(self, sender, receiver, public_key, message, signature):
        self.sender = sender
        self.receiver = receiver
        self.timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.tx_id = "B" + self.timestamp
        self.message = message
        self.public_key = public_key
        self.signature = signature

