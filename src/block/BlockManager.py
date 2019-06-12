from block.BlockStorage import BlockStorage


class BlockManager:
    def __init__(self):
        self.block_storage = BlockStorage()

    def generate_block(self, transaction_list):
        """
        generate block
        :param transaction_list: content of block
        :return:
        """
        """
        TODO
        - get last block hash
        - get block hash, nonce from pow
        - create new block header and block
        """
        pass

    def notice_making_block(self, transaction_list):
        """
        notice to make block to miner
        called from transaction manager
        :param transaction_list: content of block
        :return:
        """
        """
        TODO
        - notice to make a block to miner
        - wait for miner's response
        """
        pass

    def add_block(self, block):
        pass
