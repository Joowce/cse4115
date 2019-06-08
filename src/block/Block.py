import time


class BlockHeader(object):
    def __init__(self, prev_hash, block_hash, nonce, hash_difficulty, miner):
        self.type = 'B'
        self.block_hash = block_hash
        self.hash_difficulty= hash_difficulty
        self.miner = miner

        self.nonce = nonce
        self.prev_hash = prev_hash
        self.timestamp = time.strftime('%Y%m%d%H%M%S', time.localtime())
        self.num_transaction = 0


class Block(object):
    def __init__(self, block_header, transaction_list):
        transaction_list = transaction_list or []

        self.block_header = block_header
        self.transaction_list = transaction_list
        self.block_header.num_transaction = len(transaction_list)
