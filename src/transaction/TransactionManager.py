import service.Validator as Validator
import logging
from enum import Enum


class TransactionResult(Enum):
    Fail = -1
    Success = 1
    Full = 2


class TransactionManager:
    def __init__(self):
        self.pool = []

    def get_transaction(self, transaction):
        if Validator.valid_transaction(transaction):
            logging.error('not valid transaction')
            return TransactionResult.Fail
        self.pool.append(transaction)
        return TransactionResult.Full \
            if len(self.pool) == 10 \
            else TransactionResult.Success
