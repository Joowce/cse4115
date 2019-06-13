import hashlib


def get_hash(string):
    return hashlib.sha256(string.encode()).hexdigest()