from interface.UserInterface import start
import logging
from User.Miner import Miner
from connection.Client import Client
from connection.Message import parse_message, MessageType, wrap_block, wrap_transaction
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


def send_block(c, block):
    data = wrap_block(block)
    c.send(data)


def send_transaction(u, c, txt):
    transaction = u.generate_transaction('', txt)
    data = wrap_transaction(transaction)
    c.send(data)
    logging.info('Send transaction[%s]', transaction.tx_id)


if __name__ == '__main__':

    client = Client()

    miner = Miner()
    miner.block_manager.register_after_mine(lambda block: send_block(client, block))

    app = QtWidgets.QApplication(sys.argv)
    main_form = Form(miner.name)

    main_form.change_status_text("Miner : %s            " % miner.name)
    main_form.register_send_handler(lambda txt: send_transaction(miner, client, txt))
    main_form.register_mine_handler(miner.block_manager.start_mining)

    miner.register_notice_prompt(main_form.queue_thread.send_open_dialog)

    logger = logging.getLogger('monitoring')
    logger.addHandler(MonitoringHandler(main_form))

    start(miner, client, receive)
    sys.exit(app.exec())
