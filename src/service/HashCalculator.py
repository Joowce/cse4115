import hashlib


def get_hash(data):
    return hashlib.sha256(data).hexdigest()