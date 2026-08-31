import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


AAD = b"secure-messaging-flask-v1"


def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)


def encrypt_message(aes_key, plaintext):
    nonce = os.urandom(12)

    aesgcm = AESGCM(aes_key)

    ciphertext = aesgcm.encrypt(
        nonce,
        plaintext.encode("utf-8"),
        AAD,
    )

    return nonce, ciphertext


def decrypt_message(aes_key, nonce, ciphertext):
    aesgcm = AESGCM(aes_key)

    plaintext = aesgcm.decrypt(
        nonce,
        ciphertext,
        AAD,
    )

    return plaintext.decode("utf-8")
