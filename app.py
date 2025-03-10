import socket
import threading
import json
import uuid
from datetime import datetime

# Box Router Configuration
BOX_ROUTER_HOST = "0.0.0.0"  # Listen on all interfaces
BOX_ROUTER_PORT = 5555  # Default Box Network Port

# Routing Table (Static for Now, Later Can Be Dynamic)
routing_table = {
    "BoxNode567.BoxNet": ("127.0.0.1", 6000),  # Example Destination Node
    "BoxRouter2.BoxNet": ("127.0.0.1", 7000)  # Another Router
}

# Function to Handle Incoming Boxes
def handle_box(client_socket):
    try:
        box_data = client_socket.recv(4096).decode()
        box = json.loads(box_data)
        print(f"\n📦 Received Box: {box['id']} from {box['sender']}")
        
        destination = box["receiver"]
        
        if destination in routing_table:
            next_hop_ip, next_hop_port = routing_table[destination]
            print(f"➡ Forwarding Box to {destination} ({next_hop_ip}:{next_hop_port})")
            
            # Forward Box to Next Router/Node
            forward_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            forward_socket.connect((next_hop_ip, next_hop_port))
            forward_socket.send(json.dumps(box).encode())
            forward_socket.close()
        else:
            print(f"❌ No Route Found for {destination}. Dropping Box.")
        
    except Exception as e:
        print(f"Error Handling Box: {str(e)}")
    finally:
        client_socket.close()

# Start Box Router
def start_box_router():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((BOX_ROUTER_HOST, BOX_ROUTER_PORT))
    server_socket.listen(5)
    print(f"🚀 Box Router is Listening on Port {BOX_ROUTER_PORT}...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"📡 Connection from {addr}")
        thread = threading.Thread(target=handle_box, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_box_router()
