import time
import service.Validator as Validator
import logging
from enum import Enum


class TransactionResult(Enum):
    Fail = -1
    Success = 1
    Full = 2


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

    def add_transaction(self, transaction):
        # TODO: pass valid_transaction parameter
        if Validator.valid_transaction():
            logging.error('not valid transaction')
            return TransactionResult.Fail
        self.pool.append(transaction)
        return TransactionResult.Full \
            if len(self.pool) == 10 \
            else TransactionResult.Success
