import time
import json


class BlockHeader(object):
    def __init__(self, prev_hash, block_hash, nonce, hash_difficulty, miner_public_key):
        self.type = 'B'
        self.block_hash = block_hash
        self.hash_difficulty = hash_difficulty
        self.miner = miner_public_key

        self.nonce = nonce
        self.prev_hash = prev_hash
        self.timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.num_transaction = 0


class Block(object):
    def __init__(self, block_header=None, transaction_list=None):
        if (not block_header) or (not transaction_list):
            return
        transaction_list = transaction_list or []

        self.block_header = block_header
        dict_list = [vars(tx) for tx in transaction_list]
        self.transaction_list = json.dumps(dict_list)
        self.block_header.num_transaction = len(transaction_list)

    def load_dict(self, data):
        header = data['block_header']
        block_header = BlockHeader(header['prev_hash'],
                                   header['block_hash'],
                                   header['nonce'],
                                   header['hash_difficulty'],
                                   header['miner'])
        self.block_header = block_header
        self.transaction_list = data['transaction_list']
        self.block_header.num_transaction = len(self.transaction_list)
        return self
