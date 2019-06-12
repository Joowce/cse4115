import enum
import util.Crypto as Crypto
from transaction.TransactionManager import TransactionManager
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

    def add_neighbor(self, user):
        if user['name'] in self.neighbors_name_map:
            return
        self.neighbors_name_map[user['name']] = user
        self.neighbors_pub_map[user['public_key']] = user
        logging.info('add user %s', user)

    def generate_transaction(self):
        pass

