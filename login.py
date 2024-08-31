import tkinter as tk
import tkinter.font as tkFont
import client_services as clientservice
import socket
from tkinter import messagebox

class Login(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
       
        title_font=tkFont.Font(family="Helvetica", size=14, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=11)       

        # Title 
        title_label = tk.Label(self, text='Meeting Recorder',font=title_font)
        title_label.grid(row=0,column=0,pady=20,columnspan=2)

        # Username label and entry
        username_label = tk.Label(self, text="Username:",font=label_font)
        username_label.grid(row=1,column=0,padx=5, pady=5)
        username_entry = tk.Entry(self,font=label_font)
        username_entry.grid(row=1,column=1,padx=5, pady=5)

        # Password label and entry
        password_label = tk.Label(self, text="Password:",font=label_font)
        password_label.grid(row=2,column=0,padx=5, pady=5)
        password_entry = tk.Entry(self, show="*",font=label_font)
        password_entry.grid(row=2,column=1,padx=5, pady=5)

        # Login button
        login_button =tk.Button(self,text="Login",bg="#121212", fg="white",width=15,height=1,font=label_font,command=lambda: login(username_entry,password_entry,controller))
        login_button.grid(row=3,column=0,pady=15,columnspan=2)

def login(username_entry,password_entry,controller):      
        username = username_entry.get()
        password = password_entry.get()
        if(not username):
            return username_entry.focus()
        if(not password):
            return password_entry.focus()   
        
        user_obj={'username':username,'password':password,'ipaddress':str(socket.gethostbyname(socket.gethostname()))} 
        if(clientservice.client_login(user_obj)):
            controller.show_frame("MeetingRecord")
        else:
            messagebox.showerror("Error", "Login Failed!")


    
         
