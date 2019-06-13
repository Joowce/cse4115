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


def start(user, client, msg_handler):
    if register_user(user, client) != 1:
        logging.info('already existed user name')
        return
    t = Thread(target=msg_handler, args=(user, client))
    t.daemon = True
    t.start()

    time = 1

    while True:
        try:
            # receiver = input()
            receiver = time
            time += 1
            message = input(">>> Type Message\n")
            transaction = user.generate_transaction(receiver, message)

            if time % 3 == 0:
                prev_message = transaction.message
                transaction.message = input('*** Change Transaction Message ***\n')
                logging.info('Change transaction[%s]:  %s -> %s', transaction.tx_id, prev_message, transaction.message)

            data = wrap_transaction(transaction)
            client.send(data)
            logging.info('Send transaction[%s]', transaction.tx_id)
        except KeyboardInterrupt:
            logging.info('finish')
            break


def receive(user, client):
    msg = client.receive()

    while msg:
        message_type, data = parse_message(msg)
        if message_type == MessageType.NEIGHBOR:
            user.add_neighbor(data)
        elif message_type == MessageType.TRANSACTION:
            user.transaction_manager.add_transaction(data)
        elif message_type == MessageType.BLOCK:
            user.block_manager.add_block(data)
        elif message_type == MessageType.NEIGHBOR_LIST:
            user.init_neighbor_list(data)
        elif message_type == MessageType.LOGOUT:
            user.remove_neighbor(data)

        msg = client.receive()


if __name__ == '__main__':
    start(User(), Client(), receive)
