import enum
import json
import logging
from User.Neighbor import Neighbor
from transaction.Transaction import Transaction
from block.Block import Block, BlockHeader


class MessageType(enum.Enum):
    NEIGHBOR = 1
    TRANSACTION = 2
    BLOCK = 3
    NEIGHBOR_LIST = 4
    STRING = 5
    LOGOUT = 6


def generate_message(message_type, data):
    message = {'type': message_type.name, 'data': data}
    return json.dumps(message)


def wrap_neighbor(neighbor):
    data = neighbor.get_summary()
    return generate_message(MessageType.NEIGHBOR, data)


def wrap_transaction(transaction):
    data = vars(transaction)
    return generate_message(MessageType.TRANSACTION, data)


def wrap_neighbor_list(neighbor_list):
    summary_list = [neighbor.get_summary() for neighbor in neighbor_list]
    return generate_message(MessageType.NEIGHBOR_LIST, summary_list)


def wrap_logout(neighbor):
    data = neighbor.get_summary()
    return generate_message(MessageType.LOGOUT, data)


def wrap_block(block):
    data = vars(block)
    data['block_header'] = vars(block.block_header)
    return generate_message(MessageType.BLOCK, data)


def parse_message(message):
    message_type = MessageType.STRING
    data = message
    try:
        message = json.loads(message)
        message_type = MessageType[message['type']]
        data = message['data']

        if message_type == MessageType.NEIGHBOR_LIST:
            data = [Neighbor(total_dict=neighbor) for neighbor in data]
        elif message_type in (MessageType.NEIGHBOR, MessageType.LOGOUT):
            data = Neighbor(total_dict=data)
        elif message_type == MessageType.TRANSACTION:
            data = Transaction().load_dict(data)
        elif message_type == MessageType.BLOCK:
            data = Block().load_dict(data)
    except Exception as e:
        logging.error(e)

    return message_type, data


if __name__ == '__main__':
    parse_message('already registered')
