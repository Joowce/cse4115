import enum
import json


class MessageType(enum.Enum):
    USER = 1
    TRANSACTION = 2
    BLOCK = 3


def generate_message(type, data):
    message = {'type': type.value, 'data': data}
    return json.dumps(message)


def generate_user_message(user):
    data = {
        'name': user.get('name'),
        'public_key': user.get('public_key'),
        'addr': user.get('addr'),
        'type': user.get('type')
    }
    return generate_message(MessageType.USER, data)


def parse_message(message):
    message = json.loads(message)
    return message['type'], message['data']