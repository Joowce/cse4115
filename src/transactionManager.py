import time


def create_transaction(sender, receiver, data):
    return {
        'from': sender,
        'to': receiver,
        'data': data,
        'timestamp': time.time(),
    }

