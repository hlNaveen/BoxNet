import socket
import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# Load Keys
with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("public_key.pem", "rb") as f:
    sender_public_key = serialization.load_pem_public_key(f.read())

# Decrypt Data
def decrypt_message(encrypted_data):
    decrypted = private_key.decrypt(
        bytes.fromhex(encrypted_data),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()

# Verify Signature
def verify_signature(message, signature):
    try:
        sender_public_key.verify(
            bytes.fromhex(signature),
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False

# Start Box Server
def start_box_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 6000))
    server_socket.listen(5)

    print("🛡️ Secure Box Server is Listening on 6000...")

    while True:
        client_socket, addr = server_socket.accept()
        box_data = json.loads(client_socket.recv(4096).decode())

        print(f"📦 Box Received: {box_data['id']} from {box_data['sender']}")

        if verify_signature(decrypt_message(box_data["data"]), box_data["signature"]):
            print(f"✅ Decrypted Data: {decrypt_message(box_data['data'])}")
        else:
            print("❌ Signature Verification Failed! Possible Tampering Detected.")

        client_socket.close()

start_box_server()
