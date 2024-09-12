import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import client_socket as clientsocket
import socket
import threading
import json

# Server configuration
SERVER_IP = '192.168.99.157'#socket.gethostbyname(socket.gethostname())  # Replace with the IP address of the server Raspberry Pi
PORT = 1234# The port the server is listening on

class MeetingRecord(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller   

        # Meeting State Change
        def on_change(*args):
            status=self.meeting_status.get()
            meeting_status_label.config(text=status)

        self.meeting_status = tk.StringVar() 
        self.meeting_status.trace_add('write',on_change)

        # Font Style for Label
        self.label_font=tkFont.Font(family="Helvetica", size=10) 

        # Create Image and Show on Label
        self.image = Image.open("Assets/mic.png")
        self.photo = ImageTk.PhotoImage(self.image)       
        label = tk.Label(self, image=self.photo)
        label.pack(padx=5, pady=5)
        
        meeting_status_label = tk.Label(self,fg='Black')
        meeting_status_label.pack(padx=5, pady=5)
          
        #start & stop buttons
        startBtn=tk.Button(self,text="Start",bg="#121212", fg="white",width=15,height=2,font=self.label_font,command=lambda: start_recording())
        stopBtn=tk.Button(self,text="Stop",bg="#DEE3E2", fg="black",width=15,height=2,font=self.label_font)
        startBtn.pack(side=tk.LEFT,padx=5, pady=5)
        stopBtn.pack(side=tk.LEFT,padx=5, pady=5)   
    
        # start btn 
        def start_recording():
            client_msg='{"username":"naythithtoo","type":"client","login_date":"2024-08-30 22:52:03.961074","ipaddress":"192.168.99.157"}';
            start_record_thread = threading.Thread(target=start_client, args=(client_msg,))
            start_record_thread.start()
       

        # Function receiving message from server
        def receive_messages(client_socket):
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if not message:
                        break
                    print(f"Receive Message From Client Without Json format: {message}")
                    message_json=json.loads(message)
                    print(f"Receive Message From Client : {message_json}")
                    self.meeting_status.set(f"{message_json['username']} is recording.......")       
                except:
                    print("An error occurred. Exiting...")
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
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, PORT))

            # Start threads for receiving and sending messages
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.start()

            send_thread = threading.Thread(target=send_messages, args=(client_socket,client_message))
            send_thread.start()     
       