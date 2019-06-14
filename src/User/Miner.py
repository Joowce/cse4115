from User.User import User


class Miner(User):
    def __init__(self):
        super().__init__()
        self.block_manager.register_miner(self)
        self.notice_prompt = None

    def register_notice_prompt(self, callback):
        self.notice_prompt = callback

    def notice_making_block(self, transaction_list):
        self.notice_prompt(transaction_list)