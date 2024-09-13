import socket
import threading
import json
from Enum.actiontype import ActionType
from userloginservice import user_login

# Server configuration
HOST = '0.0.0.0'#socket.gethostbyname(socket.gethostname())#get host ip address
PORT =  8090# Port to listen on

# json to hold all connected clients
clients = {}

# Function to handle individual client connections
def handle_client(client_socket, addr):
    print(f"[Server][Connected By] : {addr}")   
    global clients  
    addr=addr[0]#only get ip address from tuple addr
    clients= {key: value for key, value in clients.items() if addr!=key} if (clients is not None) else clients
    clients[addr] = client_socket 
    print(f"[Server] [Requested Client Address List] : {clients}")
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            # Received Message and Decode Message
            decoded_message = message.decode('utf-8')
            recipient_ip, client_messsage = decoded_message.split(": ", 1)
            print(f"[Server][Server Receive Client Message]: {recipient_ip} {client_messsage}")       
            # Replace single code to double code 
            # Change to Json Format    
            client_messsage_json=json.loads(client_messsage.replace("'", '"'))              
            if(client_messsage_json['actiontype']==ActionType.LOGIN.name):              
                login_result=user_login({
                    'usercode':client_messsage_json['usercode'],
                    'usertype':client_messsage_json['usertype']
                })  
                login_result['actiontype']=ActionType.LOGIN.name
                print(f'[Server][Login Result]: {login_result}')
                clients[addr].sendall(str(login_result).encode('utf-8'))  
            else:
                print(f'[Server][Send All Clients]:{clients}')
                for client_addr, socket in clients.items():
                    print(f"[Server][Client Address] : {client_addr}")
                    print(f"[Server][Socket Name] : {socket}")     
                    socket.sendall(str(client_messsage_json).encode('utf-8'))
                            
        except Exception as err:
            print(f"[Server][Exception Error Occur] : {err}")
            break

# Set up the server socket
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[Server][Server listening on] : {socket.gethostbyname(socket.gethostname())}:{PORT}")
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

     
