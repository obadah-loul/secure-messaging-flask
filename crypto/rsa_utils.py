from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_pem, public_pem


def encrypt_private_key(private_pem, encryption_key):
    fernet = Fernet(encryption_key.encode())

    encrypted_private_key = fernet.encrypt(private_pem)

    return encrypted_private_key.decode()


def decrypt_private_key(encrypted_private_key, encryption_key):
    fernet = Fernet(encryption_key.encode())

    private_pem = fernet.decrypt(
        encrypted_private_key.encode()
    )

    return serialization.load_pem_private_key(
        private_pem,
        password=None,
    )


def load_public_key(public_pem):
    if isinstance(public_pem, str):
        public_pem = public_pem.encode()

    return serialization.load_pem_public_key(public_pem)


def encrypt_aes_key(public_pem, aes_key):
    public_key = load_public_key(public_pem)

    return public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_aes_key(
    encrypted_private_key,
    encrypted_aes_key,
    encryption_key,
):
    private_key = decrypt_private_key(
        encrypted_private_key,
        encryption_key,
    )

    return private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(
                algorithm=hashes.SHA256()
            ),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
