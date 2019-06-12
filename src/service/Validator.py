import hashlib
import util.Crypto as Crypto


def valid_transaction(transaction):
    if transaction.sender is None:
        return False

    return Crypto.verify_signature(transaction.sender,
                                   transaction.signature,
                                   transaction.get_data())


def valid_block(block):
    hash_val = hashlib.sha256(block).hexdigest()
    for i in range(2):
        if hash_val[i] != 0:
            return False
    return True
