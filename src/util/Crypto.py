from ecdsa import SigningKey, VerifyingKey, NIST384p, BadSignatureError


def generate_key():
    private_key = SigningKey.generate(curve=NIST384p)
    public_key = private_key.get_verifying_key()
    return private_key.to_string().hex(), public_key.to_string().hex()


def sign(private_key, data):
    sk = SigningKey.from_string(bytes.fromhex(private_key), curve=NIST384p)
    return sk.sign(data.encode()).hex()


def verify_signature(public_key, signature, data):
    vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=NIST384p)
    try:
        return vk.verify(bytes.fromhex(signature), data.encode())
    except BadSignatureError:
        return False


if __name__ == '__main__':
    Sk, Vk = generate_key()
    msg = input()
    sig = sign(Sk, msg)
    print(sig)
    print(verify_signature(Vk, sig, msg))
