import time
import queue
import os, sys
import logging

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtWidgets import QListWidgetItem, QGraphicsOpacityEffect

from view.node_widget import NodeWidget

monitoring_queue = queue.Queue()

Main_form = None

def log(data):
    if Main_form==None:
        logging.debug(data)
    else:
        Main_form.add_queue_data(data)

def add_peer(title, subtitle, iconfilename):
    # Main_form.add_queue_data("log."+title + " peer is added.")
    if Main_form == None:
        logging.debug(title + "("+subtitle+") peer is added.")
    else:
        Main_form.add_node(title, subtitle, iconfilename)


class ReadThread(QThread):
    add_peer_sig = pyqtSignal(str, str, str)
    log_sig = pyqtSignal(str)
    frame_sig = pyqtSignal(str)
    bl_sig = pyqtSignal(str)
    tx_sig = pyqtSignal(str)
    rm_peer_sig = pyqtSignal(str)
    full_sig = pyqtSignal([object])

    def __init__(self):
        QThread.__init__(self)

    # run method gets called when we start the thread
    def run(self):
        time.sleep(1.5)
        while True:
            self.frame_sig.emit('Server Status : NORMAL            ' + time.strftime('%H:' + '%M:' + '%S'))

            if monitoring_queue.qsize() > 0:
                datas = monitoring_queue.get()

                data = datas.split('.')

                if data[0] == 'log':
                    self.log_sig.emit(data[1])
                elif data[0] == 'block':
                    self.bl_sig.emit(data[1])
                elif data[0] == 'transaction':
                    self.tx_sig.emit(data[1])
                elif data[0] == 'add_peer':
                    print(data)
                    self.add_peer_sig.emit(data[1], data[2],
                                           os.path.join(os.path.dirname(__file__), 'static', data[3].lower() + ".png"))
                elif data[0] == 'remove_peer':
                    self.rm_peer_sig.emit(data[1])

    def send_open_dialog(self, transaction_list):
        self.full_sig.emit(transaction_list)


class Form(QtWidgets.QDialog):
    def __init__(self, name='', parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(__file__), "monitoring.ui"))

        self.mine_dialog = QtWidgets.QDialog(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), "dialog.ui"), self.mine_dialog)

        opacity_effect = QGraphicsOpacityEffect(self.mine_dialog)
        opacity_effect.setOpacity(0)

        # self.ui.setWindowFlags(Qt.SplashScreen)                          # 윈도우 타이틀 없애기

        self.ui.listWidget_4.setSpacing(30)
        if name != '':
            self.ui.label.setText(self.ui.label.text() + ': %s' % name)

        self.queue_thread = ReadThread()
        self.queue_thread.add_peer_sig.connect(self.add_node)
        self.queue_thread.log_sig.connect(self.handle_log)
        self.queue_thread.frame_sig.connect(self.change_status_text)
        self.queue_thread.bl_sig.connect(self.handle_block)
        self.queue_thread.tx_sig.connect(self.handle_tx)
        self.queue_thread.rm_peer_sig.connect(self.remove_node)
        self.queue_thread.full_sig.connect(self.open_mine_dialog)

        self.ui.pushButton.clicked.connect(self.send_sig_handler)

        self.send_handler = None
        self.mine_handler = None

        self.queue_thread.start()
        self.ui.show()

    def open_mine_dialog(self, transaction_list):
        self.mine_dialog.buttonBox.accepted.connect(lambda: self.accept_mine(transaction_list))
        self.mine_dialog.setWindowModality(Qt.ApplicationModal)
        self.mine_dialog.exec_()

    def accept_mine(self, transaction_list):
        nonce_start = self.mine_dialog.plainTextEdit.toPlainText()
        try:
            nonce_start = int(nonce_start)
        except Exception:
            nonce_start = 0
        self.mine_handler(transaction_list, nonce_start)

    def register_send_handler(self, callback):
        self.send_handler = callback

    def register_mine_handler(self, callback):
        self.mine_handler = callback

    def send_sig_handler(self):
        text = self.ui.plainTextEdit.toPlainText()
        if self.send_handler:
            self.send_handler(text)
        self.ui.plainTextEdit.setPlainText("")

    def add_node(self, title, subtitle, iconfilename):
        # Create QCustomQWidget
        myQCustomQWidget = NodeWidget(self.ui.listWidget_4)
        myQCustomQWidget.setTextUp(title)
        myQCustomQWidget.setTextDown(subtitle)
        myQCustomQWidget.setIcon(iconfilename)

        # Create QListWidgetItem
        myQListWidgetItem = QListWidgetItem(self.ui.listWidget_4)

        # Set size hint
        myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())


        # Add QListWidgetItem into QListWidget
        self.ui.listWidget_4.addItem(myQListWidgetItem)
        self.ui.listWidget_4.setItemWidget(myQListWidgetItem, myQCustomQWidget)

    def remove_node(self, index):
        self.ui.listWidget_4.removeItemWidget(self.ui.listWidget_4.takeItem(index))

    def change_status_text(self, message):
        self.ui.label_7.setText(""+message)

    def handle_log(self, log):
        print(log)
        self.add_log_item(log)
        self.change_frame_color(44, 132, 238)

    def handle_block(self, log):
        self.add_block_item(log)
        self.change_frame_color(231, 76, 60)

    def handle_tx(self, tx):
        self.add_transaction_item(tx)
        self.change_frame_color(241, 196, 15)

    def add_log_item(self,log):
        item = QListWidgetItem(log)
        self.ui.listWidget_5.addItem(item)

    def add_block_item(self,log):
        item = QListWidgetItem(log)
        self.ui.listWidget_3.addItem(item)

    def add_transaction_item(self,log):
        item = QListWidgetItem(log)
        self.ui.listWidget_2.addItem(item)

    def change_frame_color(self, r, g, b):
        stylesheet = "background-color: rgb({0}, {1}, {2})".format(r, g, b)
        widget_list = [self.ui.widget,self.ui.widget_2,self.ui.widget_3,self.ui.widget_4,self.ui.widget_5]
        
        for widget in widget_list:
            widget.setStyleSheet(stylesheet)

    @staticmethod
    def add_queue_data(data):
        monitoring_queue.put(data)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Main_form = Form()
    add_peer('test', '[\'127-0-0-1\', 51902]', os.path.join(os.path.dirname(__file__), "node.png"))
    sys.exit(app.exec())