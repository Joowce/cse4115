from interface.UserInterface import start
import logging
from User.Miner import Miner
from connection.Client import Client
from connection.Message import parse_message, MessageType, wrap_block
import sys
from PyQt5 import QtWidgets
from view.monitoring import Form
from logger.MonitoringHandler import MonitoringHandler


def receive(user, client):
    msg = client.receive()

    while msg:
        message_type, data = parse_message(msg)
        if message_type == MessageType.NEIGHBOR:
            user.add_neighbor(data)
        elif message_type == MessageType.TRANSACTION:
            user.transaction_manager.add_transaction(data, user.block_manager)
        elif message_type == MessageType.BLOCK:
            user.block_manager.add_block(data)
        elif message_type == MessageType.NEIGHBOR_LIST:
            user.init_neighbor_list(data)
        elif message_type == MessageType.LOGOUT:
            user.remove_neighbor(data)

        msg = client.receive()


def get_user_response(transaction_list):
    print(transaction_list)
    input_data = input('please type nonce start')
    return int(input_data) if input_data != '' else 0


def send_block(c, block):
    data = wrap_block(block)
    c.send(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_form = Form()

    client = Client()

    miner = Miner()
    miner.register_notice_prompt(get_user_response)
    miner.block_manager.register_after_mine(lambda block: send_block(client, block))

    main_form.change_status_text("Miner : %s            " % miner.name)

    logger = logging.getLogger('monitoring')
    logger.addHandler(MonitoringHandler(main_form))

    start(miner, client, receive)
    sys.exit(app.exec())
