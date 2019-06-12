from ecdsa import SigningKey, VerifyingKey, NIST384p


def generate_key():
    private_key = SigningKey.generate(curve=NIST384p)
    public_key = private_key.get_verifying_key()
    return str(private_key.to_string()), str(public_key.to_string())


def sign(private_key, data):
    sk = SigningKey.from_string(private_key)
    return sk.sign(data)


def verify_signature(public_key, signature, data):
    vk = VerifyingKey.from_string(public_key, NIST384p)
    return vk.verify(signature, data)
