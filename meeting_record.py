import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import client as clientsocket


class MeetingRecord(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Font Style for Label
        self.label_font=tkFont.Font(family="Helvetica", size=10) 

        # Create Image and Show on Label
        self.image = Image.open("Assets/mic.png")
        self.photo = ImageTk.PhotoImage(self.image)       
        label = tk.Label(self, image=self.photo)
        label.pack(padx=5, pady=5)
        
        loggeduser= {
            "username": "aungaung",
            "password": "123",
            "type": "client",
            "login_date": "2024-08-30 22:52:03.961074",
            "ipaddress": "192.168.99.157"
        }       
        #start & stop buttons
        startBtn=tk.Button(self,text="Start",bg="#121212", fg="white",width=15,height=2,font=self.label_font,command=lambda: clientsocket.start_client(loggeduser))
        stopBtn=tk.Button(self,text="Stop",bg="#DEE3E2", fg="black",width=15,height=2,font=self.label_font)
        startBtn.pack(side=tk.LEFT,padx=5, pady=5)
        stopBtn.pack(side=tk.LEFT,padx=5, pady=5)
