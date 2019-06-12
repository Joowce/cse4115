
class BlockStorage:
    def __init__(self):
        self.blocks = []

    def store_block(self, block):
        self.blocks.append(block)

    def get_last_block(self):
        return self.blocks[-1] if len(self.blocks) else None
