from block.BlockStorage import BlockStorage
from util.proofOfWork import proof_of_work
from block.Block import Block, BlockHeader
import service.Validator as Validator
from enum import Enum
from threading import Thread

difficulty = 2


class MiningStatus(Enum):
    IDLE = 0
    MINING = 1


class BlockManager:
    def __init__(self, user=None):
        self.block_storage = BlockStorage()
        self.user = user
        self.after_mine = None

        self.status = MiningStatus.IDLE
        self.mining_task = None
        self.found = False

    def register_miner(self, miner):
        self.user = miner

    def register_after_mine(self, after_mine):
        self.after_mine = after_mine

    def notice_making_block(self, transaction_list):
        if (not self.user) or self.status == MiningStatus.MINING:
            return

        is_making, nonce_start = self.user.notice_making_block(transaction_list)
        if not is_making:
            return
        self.start_mining(transaction_list, nonce_start)

    def start_mining(self, transaction_list, nonce_start):
        last_block = self.block_storage.get_last_block()
        prev_hash = last_block.block_hash if last_block else ''
        self.mining_task = Thread(target=self.mine,
                                  args=(prev_hash, transaction_list, nonce_start, self.after_mine), daemon=True)
        self.mining_task.start()

    def add_block(self, block):
        last_block = self.block_storage.get_last_block()
        prev_hash = last_block.block_hash

        if not Validator.valid_block(prev_hash, block):
            return

        self.block_storage.store_block(block)
        if self.status == MiningStatus.MINING:
            self.found = True

    def generate_block(self, prev_hash, transaction_list, nonce_start):
        block_hash, nonce, try_and_error = proof_of_work(prev_hash, difficulty, nonce_start, lambda: self.found)
        if try_and_error == -1:
            return None

        block_header = BlockHeader(prev_hash, block_hash, nonce, difficulty, self.user.public_key)
        block = Block(block_header, transaction_list)
        return block
        
    def mine(self, prev_hash, transaction_list, nonce_start, after_mining):
        self.status = MiningStatus.MINING
        block = self.generate_block(prev_hash, transaction_list, nonce_start)
        after_mining(block)
        self.found = False
        self.status = MiningStatus.IDLE


if __name__ == '__main__':
    bm = BlockManager()
    bm.register_after_mine(lambda a: print(a.block_header.block_hash))
    bm.start_mining([], 0)
    bm.mining_task.join()
