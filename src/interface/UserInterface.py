from connection.Client import Client
from threading import Thread
from connection.Message import MessageType, parse_message, wrap_user
from User.User import User
import logging


def get_info(user):
    return {
        'name': user.name,
        'type': user.type.name,
        'public_key': user.public_key
    }


def register_user(user, client):
    msg = wrap_user(get_info(user))
    client.send(msg)


def receive(user, client):
    msg = client.receive()
    while msg:
        print(msg)
        msg = client.receive()
    message_type, data = parse_message(msg)
    while msg:
        if message_type is MessageType.User:
            user.add_neighbor(data)
        elif message_type is MessageType.TRANSACTION:
            user.transaction_manager.add_transaction(data)
        elif message_type is MessageType.BLOCK:
            user.block_manager.add_block(data)


def start(user, client):
    t = Thread(target=receive, args=(user, client))
    t.daemon = True
    t.start()

    register_user(user, client)

    while True:
        try:
            message = input()
            client.send(message)
            transaction = user.generate_transaction(message)
            client.send(transaction)
        except KeyboardInterrupt:
            logging.info('finish')
            break


if __name__ == '__main__':
    start(User(), Client())
