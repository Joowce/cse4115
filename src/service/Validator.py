import hashlib
import util.Crypto as Crypto


def valid_transaction(transaction):
    if transaction.public_key is None:
        return False

    return Crypto.verify_signature(transaction.public_key,
                                   transaction.signature,
                                   transaction.message)


def valid_block(block):
    hash_val = hashlib.sha256(block).hexdigest()
    for i in range(2):
        if hash_val[i] is not 0:
            return False
    return True
