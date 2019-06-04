from ecdsa import VerifyingKey, NIST384p
import hashlib


def valid_transaction(public_key, signature, data):
    if public_key is None:
        return False
    vk = VerifyingKey.from_string(public_key, NIST384p)
    return vk.verify(signature, data)


def valid_block(block):
    hash_val = hashlib.sha256(block).hexdigest()
    for i in range(2):
        if hash_val[i] is not 0:
            return False
    return True
