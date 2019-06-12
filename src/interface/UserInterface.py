import logging
from connection.Client import Client
from threading import Thread
from User.User import User
from User.Neighbor import Neighbor
from connection.Message import MessageType, parse_message, \
    wrap_neighbor, wrap_transaction


def register_user(user, client):
    msg = wrap_neighbor(
        Neighbor(user.name, user.public_key, None, None, user.type)
    )
    client.send(msg)

    msg = client.receive()
    message_type, data = parse_message(msg)
    while message_type != MessageType.NEIGHBOR_LIST:
        if message_type == MessageType.STRING:
            return -1
        message_type, data = parse_message(client.receive())
    user.init_neighbor_list(data)
    logging.info('register completed')
    return 1


def receive(user, client):
    msg = client.receive()
    while msg:
        print(msg)
        msg = client.receive()
    message_type, data = parse_message(msg)
    while msg:
        if message_type is MessageType.NEIGHBOR:
            user.add_neighbor(data)
        elif message_type is MessageType.TRANSACTION:
            user.transaction_manager.add_transaction(data)
        elif message_type is MessageType.BLOCK:
            user.block_manager.add_block(data)
        elif message_type is MessageType.NEIGHBOR_LIST:
            user.init_neighbor_list(data)


def start(user, client):
    if register_user(user, client) != 1:
        logging.info('already existed user name')
        return
    t = Thread(target=receive, args=(user, client))
    t.daemon = True
    t.start()

    while True:
        try:
            receiver = input()
            message = input()
            client.send(message)
            transaction = user.generate_transaction(receiver, message)
            transaction = wrap_transaction(transaction)
            client.send(transaction)
        except KeyboardInterrupt:
            logging.info('finish')
            break


if __name__ == '__main__':
    start(User(), Client())
