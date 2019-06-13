import logging


class BlockStorage:
    def __init__(self):
        self.blocks = []

    def store_block(self, block):
        self.blocks.append(block)
        logging.info('+++ block chain [%d]', len(self.blocks))

    def get_last_block_hash(self):
        if len(self.blocks) == 0:
            return ''
        last_block = self.blocks[-1]
        return last_block.block_header.block_hash
