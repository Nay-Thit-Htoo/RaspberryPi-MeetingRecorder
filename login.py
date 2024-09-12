import json
import threading
import tkinter as tk
import tkinter.font as tkFont
from checkserver import check_server_connection
import client_server_service as clientservice
from tkinter import messagebox
from reset_server_connection import ResetServerConnection
import socket

class Login(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent_app=parent
       
        title_font=tkFont.Font(family="Helvetica", size=13, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=10)    
        label_sm_font=tkFont.Font(family="Helvetica", size=9)   

        self.client_checkbtn = tk.IntVar()
        self.client_checkbtn.set(1)

        self.chariman_checkbtn = tk.IntVar()
        self.chariman_checkbtn.set(0)
    
        # Title 
        title_label = tk.Label(self, text='Meeting Recorder',font=title_font)
        title_label.grid(row=0,column=0,pady=20,columnspan=3)

        # Username label and entry
        usercode_label = tk.Label(self, text="User Code:",font=label_font)
        usercode_label.grid(row=1,column=0,padx=5, pady=5)
        self.usercode_entry = tk.Entry(self,font=label_font)
        self.usercode_entry.grid(row=1,column=1,padx=5, pady=5,columnspan=2)

        # Password label and entry
        usertype_label = tk.Label(self, text="User Type:",font=label_font)
        usertype_label.grid(row=2,column=0,padx=5, pady=5)      
        self.chk_client_type = tk.Checkbutton(self, text='Client',variable=self.client_checkbtn,font=label_font,command=lambda: CheckUnCheck_UserType(True))
        self.chk_client_type.grid(row=2,column=1,padx=5, pady=5)
        self.chk_chariman_type = tk.Checkbutton(self, text='Chairman',variable=self.chariman_checkbtn,font=label_font,command=lambda: CheckUnCheck_UserType(False))
        self.chk_chariman_type.grid(row=2,column=2,padx=5, pady=5)

        # Login button
        login_button =tk.Button(self,text="Login",bg="#121212", fg="white",width=15,height=1,font=label_font,command=self.login)
                                # lambda: login(usercode_entry,self.client_checkbtn,controller,self.parent_app))
        login_button.grid(row=3,column=0,pady=15,columnspan=3)        
       
        # Reset Server Connection
        reset_server_label = tk.Label(self, text="Reset Server Connection?",font=label_sm_font,fg="blue",cursor="hand2")
        reset_server_label.grid(row=4,column=0,padx=5, pady=2,columnspan=3)
        reset_server_label.bind("<Button-1>", self.on_label_click)

        def CheckUnCheck_UserType(isClient):
            if(isClient):
                self.client_checkbtn.set(1)
                self.chariman_checkbtn.set(0)
            else:
                self.chariman_checkbtn.set(1)
                self.client_checkbtn.set(0)

    def on_label_click(self,event):
        ResetServerConnection(self.parent_app)

    def login(self):      
            username = self.usercode_entry.get()      
            if(not username):
                return self.usercode_entry.focus()
            
            user_type="Client"
            if(self.client_checkbtn.get()!=1):
                user_type="Chairman"        

            client_info=clientservice.read_clientInfo()
            if(client_info['server_ip']=="" or client_info==None):
                ResetServerConnection(self.parent_app)
            else:
                # Check your server ip and port are correct and server is running or not
                if(check_server_connection(client_info['server_ip'],int(client_info['server_port']))):
                    user_obj={'server_ip':client_info['server_ip'],'server_port':int(client_info['server_port']),
                              'usercode':username,
                              'usertype':user_type,
                              'actiontype': "LOGIN"                              
                              }           
                    # Start Client for Login in Server Socket          
                    self.start_client(user_obj)
                else:
                    messagebox.showerror("Error Message","Your Server isn't Running!")    

    def receive_messages(self,client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Receive Message Reply From Server Without Json format: {message}")
                message_json=(json.loads(str(message).replace("'", '"')))
                print(f"Receive Message with Json Format : {message_json}")            
                if(message_json['actiontype']=='LOGIN'):      
                    if(message_json['message_code']=='success'):
                        print(f'{message_json['message']}')
                        self.controller.show_frame('MeetingRecord')
                    else:
                        messagebox.showerror("Error Message",message_json['message'])                            

            except Exception as err:
                print(f"An error occurred. Login Page >> {err}")
                client_socket.close()
                break

    # Function to send messages to the server
    def send_messages(self,client_socket,client_message):
        print(f'Sending Client Message {client_message}')
        recipient_ip = socket.gethostbyname(socket.gethostname())
        full_message=f"{recipient_ip}: {client_message}"
        client_socket.send(full_message.encode('utf-8'))

    # Set up client socket
    def start_client(self,client_message):    
        SERVER_IP=client_message['server_ip']  
        PORT=client_message['server_port']

        to_send_message_obj={
        "usercode":client_message['usercode'],
        "usertype":client_message['usertype'],
        "actiontype":client_message['actiontype']
        }

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, PORT))

        # Start threads for receiving and sending messages
        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        receive_thread.start()

        send_thread = threading.Thread(target=self.send_messages, args=(client_socket,to_send_message_obj))
        send_thread.start()


    
            

    
         
