import socket
import threading
import Settings as appsetting
import json

# Server configuration
HOST = socket.gethostbyname(socket.gethostname())#get host ip address
PORT = 5090 # Port to listen on

# json to hold all connected clients
clients = {}

# Function to handle broadcasting messages to all or specific clients
def broadcast(message, sender_socket=None, recipient_socket=None):
    if recipient_socket:
        # Send to a specific client
        try:
            recipient_socket.send(message)
        except:
            pass
    else:
        # Broadcast to all clients except the sender
        for client in clients.values():
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    pass

# Function to handle individual client connections
def handle_client(client_socket, addr):
    print(f"[Connected By] : {addr}")
    clients[addr] = client_socket 
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            # Received Message and Decode Message
            decoded_message = message.decode('utf-8')
            # Reply to Clients
            recipient_ip, msg = decoded_message.split(": ", 1) 
            print(f'\n[Received Message] : IP Address={recipient_ip} Message={msg}')

            for client_addr, socket in clients.items():
                print(f"[Client Address] : {client_addr}")
                print(f"[Socket Name] : {socket}")
                recipient_socket = socket               
                if recipient_socket:
                    broadcast(("Reply from server: Seen!").encode('utf-8'), sender_socket=client_socket, recipient_socket=recipient_socket)
                else:
                    client_socket.send(f"Client with IP {recipient_ip} not found.".encode('utf-8'))
        except:
            break

    print(f"[Disconnected By] : {addr}")
    del clients[addr]
    client_socket.close()

# Set up the server socket
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
