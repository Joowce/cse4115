import enum
import util.Crypto as Crypto
from transaction.TransactionManager import TransactionManager
from transaction.Transaction import Transaction
from block.BlockManager import BlockManager
import logging

logger = logging.getLogger('monitoring')


class UserType(enum.Enum):
    USER = 1
    MINER = 2


class User(object):
    def __init__(self):
        self.neighbors_name_map = {}
        self.neighbors_pub_map = {}
        self.neighbors = []
        self.name = input('Type user name: ')
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
        self.neighbors.append(user)
        logger.info('add_peer.%s.%s.%s', user.name, str(user.addr).replace('.', '-').replace('\'', ''), user.type.name)
        logger.info('log.+++ add user %s %s', str(user.addr).replace('.', '-'), user.name)

    def remove_neighbor(self, user):
        if user.name not in self.neighbors_name_map:
            return
        del(self.neighbors_pub_map[user.public_key])
        del(self.neighbors_name_map[user.name])
        idx = self.neighbors.index(user)
        logger.info('remove_peer.%s', idx)
        logger.info('log.--- logout user %s %s', str(user.addr).replace('.', '-'), user.name)

    def generate_transaction(self, receiver, message):
        transaction = Transaction(
            self.public_key, receiver, message,
        )
        signature = Crypto.sign(self.private_key, transaction.get_data())
        transaction.add_signature(signature)
        return transaction


if __name__ == '__main__':
    print(UserType['USER'].name)