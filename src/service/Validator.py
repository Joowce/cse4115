from ecdsa import VerifyingKey, NIST384p
import hashlib


def valid_transaction(transaction):
    if transaction.public_key is None:
        return False
    vk = VerifyingKey.from_string(transaction.public_key, NIST384p)
    return vk.verify(transaction.signature, transaction.message)


def valid_block(block):
    hash_val = hashlib.sha256(block).hexdigest()
    for i in range(2):
        if hash_val[i] is not 0:
            return False
    return True
