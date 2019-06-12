import connection.Client as Client
import enum
import util.Crypto as Crypto


class UserType(enum.Enum):
    USER = 1
    MINER = 2


class User(object):
    def __init__(self):
        """
        TODO
        1. users
        """
        self.users = []
        self.name = input('input user name:')
        self.type = UserType.USER
        self.private_key, self.public_key = Crypto.generate_key()

    def get_info(self):
        return {
            'name': self.name,
            'type': self.type.name,
            'public_key': self.public_key
        }


if __name__ == '__main__':
    user = User()
    Client.start(user.get_info(), print, input)
