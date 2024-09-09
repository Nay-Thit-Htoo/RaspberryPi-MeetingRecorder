import tkinter as tk
import tkinter.font as tkFont
import client_services as clientservice
import socket
from tkinter import messagebox
from reset_server_connection import ResetServerConnection

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
        username_label = tk.Label(self, text="User Code:",font=label_font)
        username_label.grid(row=1,column=0,padx=5, pady=5)
        username_entry = tk.Entry(self,font=label_font)
        username_entry.grid(row=1,column=1,padx=5, pady=5,columnspan=2)

        # Password label and entry
        usertype_label = tk.Label(self, text="User Type:",font=label_font)
        usertype_label.grid(row=2,column=0,padx=5, pady=5)      
        chk_client_type = tk.Checkbutton(self, text='Client',variable=self.client_checkbtn,font=label_font,command=lambda: CheckUnCheck_UserType(True))
        chk_client_type.grid(row=2,column=1,padx=5, pady=5)
        chk_chariman_type = tk.Checkbutton(self, text='Chairman',variable=self.chariman_checkbtn,font=label_font,command=lambda: CheckUnCheck_UserType(False))
        chk_chariman_type.grid(row=2,column=2,padx=5, pady=5)

        # Login button
        login_button =tk.Button(self,text="Login",bg="#121212", fg="white",width=15,height=1,font=label_font,command=lambda: login(username_entry,controller))
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

    def on_label_click(self, event):
        ResetServerConnection(self.parent_app)

def login(username_entry,controller):      
        username = username_entry.get()      
        if(not username):
            return username_entry.focus()       
        
        user_obj={'username':username,'ipaddress':str(socket.gethostbyname(socket.gethostname()))} 
        if(clientservice.client_login(user_obj)):
            controller.show_frame("MeetingRecord")
        else:
            messagebox.showerror("Error", "Login Failed!")


    
         
