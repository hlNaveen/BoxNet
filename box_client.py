import socket
import json
import uuid
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization, hashes

# Load Keys
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("public_key.pem", "rb") as f:
    receiver_public_key = serialization.load_pem_public_key(f.read())

# Encrypt Data
def encrypt_message(message):
    encrypted = receiver_public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

# Sign Data
def sign_message(message):
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

# Create Secure Box
def create_box(sender, receiver, data):
    encrypted_data = encrypt_message(data)
    signature = sign_message(data)

    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "sender": sender,
        "receiver": receiver,
        "data": encrypted_data.hex(),
        "signature": signature.hex(),
    }

# Send Box
def send_box():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 6000))

    box = create_box("BoxNode123.BoxNet", "BoxNode567.BoxNet", "Hello, this is a Secure Box!")
    client_socket.send(json.dumps(box).encode())

    print(f"✅ Sent Secure Box: {box['id']} to {box['receiver']}")
    client_socket.close()

send_box()
