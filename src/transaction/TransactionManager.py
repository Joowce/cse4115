from service import Validator
from transaction.TransactionStorage import TransactionStorage
import logging
from enum import Enum

logger = logging.getLogger('monitoring')


class TransactionResult(Enum):
    Fail = -1
    Success = 1


class TransactionManager:
    def __init__(self):
        self.pool = TransactionStorage()

    def add_transaction(self, transaction, block_manager=None):
        if not Validator.valid_transaction(transaction):
            logger.error('transaction.--- Invalid transaction[%s]: %s',
                         transaction.tx_id,
                         transaction.message)
            logger.error('transaction.--- remove invalid transaction')
            return TransactionResult.Fail

        self.pool.store_transaction(transaction)
        logger.info('transaction.+++ Store transaction[%s]: %s', transaction.tx_id, transaction.message)

        if self.pool.is_full() and block_manager:
            logger.info("transaction.pool has new 10 transactions -> notice to block manager")
            block_manager.notice_making_block(self.pool.get_last())

        return TransactionResult.Success
