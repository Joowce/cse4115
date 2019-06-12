from service import Validator
from transaction.TransactionStorage import TransactionStorage
import logging
from enum import Enum


class TransactionResult(Enum):
    Fail = -1
    Success = 1


class TransactionManager:
    def __init__(self):
        self.pool = TransactionStorage()

    def add_transaction(self, transaction, block_manager):
        if Validator.valid_transaction(transaction):
            logging.error('not valid transaction')
            return TransactionResult.Fail

        self.pool.store_transaction(transaction)

        if self.pool.is_full() and block_manager:
            logging.info("pool has new 10 transactions -> notice to block manager")
            block_manager.notice_making_block(self.pool.get_last())

        return TransactionResult.Success

