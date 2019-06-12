import enum
import util.Crypto as Crypto
from transaction.TransactionManager import TransactionManager
from transaction.Transaction import Transaction
from block.BlockManager import BlockManager
import logging


class UserType(enum.Enum):
    USER = 1
    MINER = 2


class User(object):
    def __init__(self):
        self.neighbors_name_map = {}
        self.neighbors_pub_map = {}
        self.name = input('input user name:')
        self.type = UserType.USER
        self.private_key, self.public_key = Crypto.generate_key()

        self.transaction_manager = TransactionManager()
        self.block_manager = BlockManager()

    def init_neighbor_list(self, neighbor_list):
        for neighbor in neighbor_list:
            self.add_neighbor(neighbor)

    def add_neighbor(self, user):
        if user.name in self.neighbors_name_map:
            return
        self.neighbors_name_map[user.name] = user
        self.neighbors_pub_map[user.public_key] = user
        logging.info('add user %s %s', user.name, user.addr)

    def generate_transaction(self, receiver, message):
        transaction = Transaction(
            self.public_key, receiver, message,
        )
        signature = Crypto.sign(self.private_key, transaction.get_data())
        transaction.add_signature(signature)
        return transaction


if __name__ == '__main__':
    print(UserType['USER'].name)