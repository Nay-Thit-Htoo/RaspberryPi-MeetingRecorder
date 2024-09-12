import socket
import threading
import json
import meeting_record as metRecord

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Receive Message From Server Without Json format: {message}")
            message_json=json.loads(str(message).replace("'", '"'))
            print(f"Receive Message From Server : {message_json}")            
            if(not message_json['actiontype']=='LOGIN'):         
                metRecord.set_state(f"{message_json['username']} is recording.......")                

        except Exception as err:
            print(f"An error occurred. Exiting... {err}")
            client_socket.close()
            break

# Function to send messages to the server
def send_messages(client_socket,client_message):
    print(f'Sending Client Message {client_message}')
    recipient_ip = socket.gethostbyname(socket.gethostname())
    full_message=f"{recipient_ip}: {client_message}"
    client_socket.send(full_message.encode('utf-8'))

# Set up client socket
def start_client(client_message):    
    SERVER_IP=client_message['server_ip']  
    PORT=client_message['server_port']

    to_send_message={
     "usercode":client_message['usercode'],
     "usertype":client_message['usertype'],
     "actiontype":client_message['actiontype']
    }

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, PORT))

    # Start threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,to_send_message))
    send_thread.start()
