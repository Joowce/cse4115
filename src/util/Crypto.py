from ecdsa import SigningKey, VerifyingKey, NIST384p


def generate_key():
    private_key = SigningKey.generate(curve=NIST384p)
    public_key = private_key.get_verifying_key()
    return private_key.to_string().hex(), public_key.to_string().hex()


def sign(private_key, data):
    sk = SigningKey.from_string(bytes.fromhex(private_key), curve=NIST384p)
    return sk.sign(data.encode())


def verify_signature(public_key, signature, data):
    vk = VerifyingKey.from_string(bytes.fromhex(public_key), curve=NIST384p)
    return vk.verify(signature, data.encode())


if __name__ == '__main__':
    Sk, Vk = generate_key()
    print(bytes.fromhex(Sk))
    msg = input()
    sig = sign(Sk, msg)
    print(verify_signature(Vk, sig, msg))
