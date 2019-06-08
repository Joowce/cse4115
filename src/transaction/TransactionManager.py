from service import Validator
from block import BlockManager
import logging
from enum import Enum


class TransactionResult(Enum):
    Fail = -1
    Success = 1


class TransactionManager:
    def __init__(self):
        self.pool = []

    def get_transaction(self, transaction):
        if Validator.valid_transaction(transaction):
            logging.error('not valid transaction')
            return TransactionResult.Fail

        self.pool.append(transaction)

        if len(self.pool) % 10 == 0:
            logging.info("pool has new 10 transactions -> notice to block manager")
            BlockManager.notice_making_block(self.pool[-10:])

        return TransactionResult.Success
