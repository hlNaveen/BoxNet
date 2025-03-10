from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import os

# Secure key storage (never store raw keys in memory)
def generate_secure_key(master_key):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.urandom(16),
        info=b"BoxNet Secure Key",
    )
    return hkdf.derive(master_key)
