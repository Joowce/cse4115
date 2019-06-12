import enum
import json
import logging
from User.Neighbor import Neighbor


class MessageType(enum.Enum):
    NEIGHBOR = 1
    TRANSACTION = 2
    BLOCK = 3
    NEIGHBOR_LIST = 4
    STRING = 5


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


def parse_message(message):
    message_type = MessageType.STRING
    data = message
    try:
        message = json.loads(message)
        message_type = MessageType[message['type']]
        data = message['data']

        if message_type == MessageType.NEIGHBOR_LIST:
            data = [Neighbor(total_dict=neighbor) for neighbor in data]
        elif message_type == MessageType.NEIGHBOR:
            data = Neighbor(total_dict=data)
    except Exception as e:
        logging.error(e)

    return message_type, data


if __name__ == '__main__':
    parse_message('already registered')
