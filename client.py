import socket
import threading

# Server configuration
SERVER_IP = socket.gethostbyname(socket.gethostname())  # Replace with the IP address of the server Raspberry Pi
PORT = 5090# The port the server is listening on

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            print("An error occurred. Exiting...")
            client_socket.close()
            break

# Function to send messages to the server
def send_messages(client_socket):
    while True:
        recipient_ip = socket.gethostbyname(socket.gethostname())
        message = input("Enter message: ")
        if recipient_ip:
            # Format message to send to a specific client
            full_message = f"{recipient_ip}: {message}"
        else:
            # Broadcast message to all clients
            full_message = message

        client_socket.send(full_message.encode('utf-8'))

# Set up client socket
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))

    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()


if __name__ == "__main__":
    start_client()
