import tkinter as tk
from tkinter import messagebox
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
        
        self.socket_thread = threading.Thread(target=self.start_client,args=(None,), daemon=True)
        self.socket_thread.start()

                
    # start recording
    def start_recording(self):       
        self.logged_user_info=clientservice.read_clientInfo()
        meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.START_RECORD.name                      
                    }
        print(f"[Meeting Record][Start Record] : {meeting_record_obj}")
        self.start_client(meeting_record_obj)
        
    # stop recording
    def stop_recording(self):
        meeting_status=self.meeting_status_label.cget('text')
        if(meeting_status is not None or meeting_status !=""):
            self.logged_user_info=clientservice.read_clientInfo()
            meeting_record_obj={"usercode":self.logged_user_info['usercode'],
                    "usertype":self.logged_user_info['usertype'],
                    "actiontype":ActionType.STOP_RECORD.name                      
                    }
            print(f"[Meeting Record][Stop Record] : {meeting_record_obj}")
            self.start_client(meeting_record_obj)
       
        # Function receiving message from server
    
    # Receive Message via Client Socket
    def receive_messages(self,client_socket):
        print(f"Meeting Record][Receive Message]")
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"[Meeting Record][Receive Message Reply From Server] : {message}")
                response_message=json.loads(message.replace("'", '"')) 
                print(f"[Meeting Record][Action Type]: {response_message['actiontype']}") 
                if(response_message['actiontype']==ActionType.START_RECORD.name): 
                   self.change_meeting_status_after_startrecord(response_message)
                elif(response_message['actiontype']==ActionType.OPEN_RECORD.name):
                    self.folder_create_result_show(response_message)
                else:
                  self.clear_meeting_status_enable_buttons()      

            except Exception as err:
                print(f"[Meeting Record]:[Exception Error] : {err}")                
                break
            except ConnectionAbortedError as connError:
               print(f"[Meeting Record]:[Connection Aborted Error] : {connError}")                
               break 

    # Change Meeting Status and Disable or Enable Start and Stop Buttons
    def change_meeting_status_after_startrecord(self,response):
        self.meeting_status_label.config(text=f"{response['usercode']} is recording.......")
        if(self.logged_user_info['usercode']==response['usercode']):      
            self.startBtn.config(state='disabled')                                    
        else:
            if(self.logged_user_info['usercode'].lower()=='chairman'):
                self.startBtn.config(state='normal')
                self.stopBtn.config(state='normal') 
            else:
                self.startBtn.config(state='disabled')
                self.stopBtn.config(state='disabled')

    # Create Folder After PageLoaded
    def folder_create_result_show(self,response):
        if("message_code" in response and response['message_code']=="fail"):
            messagebox.showerror("Folder Creation Message",response['message'])
            self.clear_meeting_status_enable_buttons()
   
   # Clean meeting status and enable start & stop buttons
    def clear_meeting_status_enable_buttons(self):
        self.meeting_status_label.config(text="")   
        self.startBtn.config(state='normal')
        self.stopBtn.config(state='normal')

    # Function to send messages to the server
    def send_messages(self,client_socket,client_message): 
        print(f"[Meeting Record][Send Client Message] : {client_message}")
        recipient_ip = socket.gethostbyname(socket.gethostname())
        full_message=f"{recipient_ip}: {client_message}"
        client_socket.send(full_message.encode('utf-8'))
    
    # Set up client socket
    def start_client(self,client_message):    
        self.logged_user_info=clientservice.read_clientInfo()
        logged_user_server_ip=self.logged_user_info['server_ip']
        logged_user_server_port=int(self.logged_user_info['server_port']) 
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)     
        client_socket.connect((logged_user_server_ip, logged_user_server_port))        

        # Start threads for receiving and sending messages
        receive_msg_thread = threading.Thread(target=self.receive_messages,args=(client_socket,),daemon=True)
        receive_msg_thread.start()    
        
        empty_obj={"usercode":self.logged_user_info['usercode'],"usertype": self.logged_user_info['usertype'],"actiontype":ActionType.OPEN_RECORD.name}
        client_message=client_message if (client_message is not None) else empty_obj
        send_mesg_thread = threading.Thread(target=self.send_messages, args=(client_socket, client_message,))
        send_mesg_thread.start()
        
       

    