import socket
import threading
import json
from Enum.actiontype import ActionType
from Settings import server_service
from file_service import FileService
from userloginservice import user_login

# json to hold all connected clients
clients = {}
class ServerSocket:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None
        self.server_is_running=False
    
    # Set up the server socket
    def start_server(self):
        if(self.server_is_running):
            return
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.server_is_running = True
        clean_user_thread=threading.Thread(target=server_service.clean_clients)
        clean_user_thread.start()     
        print(f"[Server][Server listening on] : {socket.gethostbyname(socket.gethostname())}:{self.port}")
        threading.Thread(target=self.accept_connections, daemon=True).start() 

    def accept_connections(self):
        while self.server_is_running:
            try:
                client_socket, addr = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.start()     
            except OSError as e:
                # Handle the case where the server socket is closed
                if not self.server_is_running:
                    break
                print("[Server Socket]: [Socket Error]", e)

    # Function to handle individual client connections
    def handle_client(self,client_socket, addr):
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
                    print(f"[Server][Login Result]: {login_result}")                
                    clients[addr].sendall(str(login_result).encode('utf-8'))  
                if(client_messsage_json['actiontype']==ActionType.OPEN_RECORD.name): 
                    print(f"[Server][Folder Create for]: {client_messsage_json['usercode']}")
                    # if(not create_folder_with_usercode(client_messsage_json['usercode'])):
                    #     client_messsage_json["message"]="Folder Creation Failed!"
                    #     client_messsage_json["message_code"]="fail"
                    # else:                    
                    current_record_user=self.get_recording_user()  
                    client_messsage_json=client_messsage_json if current_record_user is None else current_record_user
                    clients[addr].sendall(str(client_messsage_json).encode('utf-8'))  
                else:
                    if(client_messsage_json['actiontype']==ActionType.START_RECORD.name):
                        server_service.update_recording_client_info(client_messsage_json,is_start_recording=True)
                    elif(client_messsage_json['actiontype']==ActionType.STOP_RECORD.name):
                        server_service.update_recording_client_info(client_messsage_json,is_start_recording=False)
                    print(f"[Server][Send All Clients]:{clients}")
                    for client_addr, socket in clients.items():
                        print(f"[Server][Client Address] : {client_addr}")
                        print(f"[Server][Socket Name] : {socket}")     
                        socket.sendall(str(client_messsage_json).encode('utf-8'))
                                
            except Exception as err:
                print(f"[Server][Exception Error Occur] : {err}")
                break

    # Stop Server
    def stop_server(self):
        if not self.server_is_running:
                return
        self.server_is_running=False
        self.server_socket.close()
        print("[Server]Server stopped....")       
        
    # Create Folder When Client's Meeting Record Page Open
    def create_folder_with_usercode(usercode):
        server_setting_data=server_service.read_setting_data()
        if(server_setting_data is None or server_setting_data['upload_file_path'] is None):
            print(f'Server Upload Folder Path Not Found!')
            return False           
        server_folder_path=server_setting_data['upload_file_path']    
        file_service = FileService(usercode, server_folder_path)
        file_service.create_folder()
        return True   

    # Get current recording user
    def get_recording_user(self):
        current_record_user=server_service.get_current_recording_user()
        if(len(current_record_user)>0 and current_record_user is not None):
            current_record_user=current_record_user[0]
            current_record_user['actiontype']=ActionType.OPEN_RECORD.name
            current_record_user['message_code']='success'
            current_record_user['message']=f"{current_record_user['usercode']} is recording...."
            return current_record_user
        return None