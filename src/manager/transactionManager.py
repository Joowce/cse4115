import time


class TransactionManager:
    def __init(self):
        self.pool = []

    @staticmethod
    def create_transaction(self, sender, receiver, data):
        return {
            'from': sender,
            'to': receiver,
            'data': data,
            'timestamp': time.time(),
        }
