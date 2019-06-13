import util.Crypto as Crypto
from service.HashCalculator import get_hash


def valid_transaction(transaction):
    if transaction.sender is None:
        return False

    return Crypto.verify_signature(transaction.sender,
                                   transaction.signature,
                                   transaction.get_data())


def valid_block(prev_hash, block_header):
    if block_header.prev_hash != prev_hash:
        return False

    target = 2 ** (256 - block_header.hash_difficulty)
    hash_val = get_hash(str(prev_hash) + str(block_header.nonce))
    return int(hash_val, 16) <= target
