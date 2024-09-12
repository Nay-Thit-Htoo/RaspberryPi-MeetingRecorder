import socket
import threading
import json

from userloginservice import user_login

# Server configuration
HOST = '0.0.0.0'#socket.gethostbyname(socket.gethostname())#get host ip address
PORT =  8090# Port to listen on

# json to hold all connected clients
clients = {}

# Function to handle individual client connections
def handle_client(client_socket, addr):
    print(f"[Connected By] : {addr}")
    clients[addr] = client_socket 
    # print(f"Client Address : {clients}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            # Received Message and Decode Message
            decoded_message = message.decode('utf-8')
            recipient_ip, client_messsage = decoded_message.split(": ", 1)
            print(f"Server Receive Client Message: {recipient_ip} {client_messsage}")       
            # Replace single code to double code 
            # Change to Json Format    
            client_messsage_json=json.loads(client_messsage.replace("'", '"'))  
            if(client_messsage_json['actiontype']=='LOGIN'):
                login_result=user_login({
                    'usercode':client_messsage_json['usercode'],
                    'usertype':client_messsage_json['usertype']
                })  
                login_result['actiontype']='LOGIN'
                print(f'Login Result: {login_result}')
                clients[addr].sendall(str(login_result).encode('utf-8'))  
            else:
                for client_addr, socket in clients.items():
                    print(f"[Client Address] : {client_addr}")
                    print(f"[Socket Name] : {socket}")                         
                    socket.sendall(client_messsage_json.encode('utf-8'))
                            
        except Exception as err:
            print(f"[Face Excepiton] : {addr} and Error Occur {err}")
            break

# Set up the server socket
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Server listening on {socket.gethostbyname(socket.gethostname())}:{PORT}")
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

     # Reply to Clients
                # recipient_ip, msg = decoded_message.split(": ", 1)           
                # print(f'\n[Received Message] : IP Address={recipient_ip} Message={msg}')
