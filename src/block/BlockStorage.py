import logging
logger = logging.getLogger('monitoring')


class BlockStorage:
    def __init__(self):
        self.blocks = []

    def store_block(self, block):
        self.blocks.append(block)
        logger.info('block.[%s] %s', block.block_header.block_id, block.block_header.block_hash)

    def get_last_block_hash(self):
        if len(self.blocks) == 0:
            return ''
        last_block = self.blocks[-1]
        return last_block.block_header.block_hash
