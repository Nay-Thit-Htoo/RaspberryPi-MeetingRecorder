import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import client_server_service as clientservice
import socket
import threading
import json

from Enum.actiontype import ActionType

class MeetingRecord(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller 
        self.logged_user_info=None  

        # Font Style for Label
        self.label_font=tkFont.Font(family="Helvetica", size=10) 

        # Create Image and Show on Label
        self.image = Image.open("Assets/mic.png")
        self.photo = ImageTk.PhotoImage(self.image)       
        label = tk.Label(self, image=self.photo)
        label.pack(padx=5, pady=5)
        
        self.meeting_status_label = tk.Label(self,fg='Black')
        self.meeting_status_label.pack(padx=5, pady=5)
          
        #start & stop buttons
        self.startBtn=tk.Button(self,text="Start",bg="#121212", fg="white",width=15,height=2,font=self.label_font,command=self.start_recording)
        self.startBtn.pack(side=tk.LEFT,padx=5, pady=5)
        
        self.stopBtn=tk.Button(self,text="Stop",bg="#DEE3E2", fg="black",width=15,height=2,font=self.label_font,command=self.stop_recording)
        self.stopBtn.pack(side=tk.LEFT,padx=5, pady=5)   
    
    # start btn 
    def start_recording(self):
        self.logged_user_info=clientservice.read_clientInfo()
        meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.START_RECORD.name                      
                    }
        print(f'[Meeting Record][Start Record] : {meeting_record_obj}')
        start_record_thread = threading.Thread(target=self.start_client, args=(meeting_record_obj,))
        start_record_thread.start()
     # stop btn 
    
    # stop btn
    def stop_recording(self):
        meeting_status=self.meeting_status_label.cget('text')
        if(meeting_status is not None or meeting_status !=""):
            self.logged_user_info=clientservice.read_clientInfo()
            meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.STOP_RECORD.name                      
                    }
            print(f'[Meeting Record][Stop Record] : {meeting_record_obj}')
            stop_record_thread = threading.Thread(target=self.start_client, args=(meeting_record_obj,))
            stop_record_thread.start()
       
        # Function receiving message from server
    
    def receive_messages(self,client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"[Meeting Record][Receive Message Reply From Server] : {message}")
                response_message=json.loads(message.replace("'", '"')) 
                print(f'[Meeting Record][Action Type]: {response_message['actiontype']}')
                if(self.logged_user_info['usercode']==response_message['usercode']):                 
                    if(response_message['actiontype']==ActionType.START_RECORD.name): 
                        self.meeting_status_label.config(text=f"{response_message['usercode']} is recording.......")
                        self.startBtn.config(state='disabled')
                    else:
                        self.startBtn.config(state='normal')
                        self.meeting_status_label.config(text="")                       
                else:
                    if(self.logged_user_info['usercode'].tolower()!='chairman'):
                        if(response_message['actiontype']==ActionType.START_RECORD.name):
                            self.startBtn.config(state='disabled')
                            self.stopBtn.config(state='disabled') 
                        else:
                            self.startBtn.config(state='normal')
                            self.stopBtn.config(state='normal') 
                    self.meeting_status_label.config(text="")                    
            except Exception as err:
                print(f"[Meeting Record]:[Exception Error] : {err}")
                client_socket.close()
                break

    # Function to send messages to the server
    def send_messages(self,client_socket,client_message):
        print(f'[Meeting Record][Send Client Message] : {client_message}')
        recipient_ip = socket.gethostbyname(socket.gethostname())
        full_message=f"{recipient_ip}: {client_message}"
        client_socket.send(full_message.encode('utf-8'))

    # Set up client socket
    def start_client(self,client_message):    
        # Get Local Host name 
        #local_ip_address=socket.gethostbyname(socket.gethostname())

        # Get Logged User's Server IP Address and Port Number
        logged_user_server_ip=self.logged_user_info['server_ip']
        logged_user_server_port=int(self.logged_user_info['server_port'])        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Create Client Socket  
        # Check Local address and logged server ip address 
        # logged_user_server_port=(logged_user_server_port+100) if(local_ip_address!=logged_user_server_ip) else logged_user_server_port
        # client_socket.bind((local_ip_address,logged_user_server_port))# Bind Local IP Address with Custom Port Number        
        client_socket.connect((logged_user_server_ip,logged_user_server_port)) # Start Connect To Server

        # Start threads for receiving and sending messages
        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        receive_thread.start()
        send_thread = threading.Thread(target=self.send_messages, args=(client_socket,client_message,))
        send_thread.start()     
       