import logging


BLOCK_LEN = 2


class TransactionStorage:
    def __init__(self):
        self.pool = []

    def store_transaction(self, transaction):
        self.pool.append(transaction)
        logging.info('+++ transaction storage [%d]', len(self.pool))

    def is_full(self):
        return len(self.pool) % BLOCK_LEN == 0

    def get_last(self):
        return self.pool[-BLOCK_LEN:]