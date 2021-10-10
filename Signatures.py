from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization


def generate_keys():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = private.public_key()
    pu_ser = public.public_bytes(encoding=serialization.Encoding.PEM,
                              format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return private, pu_ser


def sign(message, private):
    sig = private.sign(message,
                       padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                   salt_length=padding.PSS.MAX_LENGTH),
                       hashes.SHA256())
    return sig


def verify(message, sig, pu_ser):
    loaded_pu = serialization.load_pem_public_key(pu_ser)
    try:
        loaded_pu.verify(sig,
                         message,
                         padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                     salt_length=padding.PSS.MAX_LENGTH),
                         hashes.SHA256())
        return True
    except InvalidSignature:
        return False
    # except:
    #     print("Something wrong has happened")
    #     return False


if __name__ == '__main__':
    pr, pu = generate_keys()
    pr2, pu2 = generate_keys()
    mess = b"this is a secret message"
    mess2 = b"other message"
    signature2 = sign(mess2, pr2)
    signature = sign(mess, pr)
    print(signature)
    correct = verify(mess2, signature2, pu2)

    if correct:
        print("Success! Good signature")
    else:
        print("ERROR! Signature is bad!!!")
