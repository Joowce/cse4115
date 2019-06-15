import logging

logger = logging.getLogger('monitoring')
BLOCK_LEN = 3


class TransactionStorage:
    def __init__(self):
        self.pool = []

    def store_transaction(self, transaction):
        self.pool.append(transaction)
        logger.info('+++ transaction storage [%d]', len(self.pool))
        logger.info('transaction.[%s] %s', transaction.tx_id, transaction.message)

    def is_full(self):
        return len(self.pool) % BLOCK_LEN == 0

    def get_last(self):
        return self.pool[-BLOCK_LEN:]