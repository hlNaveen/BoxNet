from pqcrypto.kem.kyber import generate_keypair, encrypt, decrypt

# Generate quantum-safe keys
public_key, private_key = generate_keypair()

# Encrypt Box using Kyber
def encrypt_data(data):
    ciphertext, secret = encrypt(public_key)
    return ciphertext.hex()

# Decrypt Box
def decrypt_data(ciphertext):
    secret = decrypt(bytes.fromhex(ciphertext), private_key)
    return secret.decode()
