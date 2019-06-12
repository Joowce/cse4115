
class TransactionStorage:
    def __init__(self):
        self.pool = []

    def store_transaction(self, transaction):
        self.pool.append(transaction)

    def is_full(self):
        return len(self.pool) % 10 == 0

    def get_last(self):
        return self.pool[-10:]