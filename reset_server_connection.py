import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from checkserver import check_server_connection
import client_server_service
import re

class ResetServerConnection:
    def __init__(self, parent_app):  
        self.parent_app=parent_app       

        title_font=tkFont.Font(family="Helvetica", size=14, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=11) 
        button_font=tkFont.Font(family="Helvetica", size=12)   
      
        width=400
        height=200 
        screen_width = self.parent_app.winfo_screenwidth()
        screen_height = self.parent_app.winfo_screenheight()

         # Calculate the position to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
     
        
        dialog = tk.Toplevel(parent_app)
        dialog.title("Reset Server Configuration")           
        # dialog.iconbitmap('Assets/recording-icon.ico')
        dialog.geometry(f'{width}x{height}+{x}+{y}') # Set the geometry of the window   

        # Register for Validate Key Press for only digit  
        validate_keypress=(dialog.register(self.validate_number_input), '%S')

        # Create a frame to hold the widgets
        frame = tk.Frame(dialog)
        frame.pack(expand=True)

        # Title 
        title_label = tk.Label(frame, text='Configuration Server Connection',font=title_font)
        title_label.grid(row=0,column=0,pady=20,columnspan=2)

        # IP Address label and entry
        ipaddress_label = tk.Label(frame, text="IP Address:",font=label_font)
        ipaddress_label.grid(row=1,column=0,padx=5, pady=5)
        ipaddress_entry = tk.Entry(frame,font=label_font)
        ipaddress_entry.grid(row=1,column=1,padx=5, pady=5,columnspan=2)
       
        # Port Number label and entry
        portnumber_label = tk.Label(frame, text="Port Number:",font=label_font)
        portnumber_label.grid(row=2,column=0,padx=5, pady=5)
        portnumber_entry = tk.Entry(frame,font=label_font,validate='key',validatecommand=validate_keypress)
        portnumber_entry.grid(row=2,column=1,padx=5, pady=5)

        # Login button
        save_button =tk.Button(frame,text="Save",bg="#121212", fg="white",width=15,height=1,font=button_font,command=lambda: save_server_configuration(dialog,ipaddress_entry,portnumber_entry))
        save_button.grid(row=3,column=0,pady=15,columnspan=3)       

    def validate_number_input(self,char):
        # Allow only digits
        return char.isdigit() or char == ""

   
def save_server_configuration(dialog,ipaddress_entry,portnumber_entry):
    ipaddress = ipaddress_entry.get()      
    if(not ipaddress):
        return ipaddress_entry.focus()       

    port_number = portnumber_entry.get()      
    if(not port_number):
        return portnumber_entry.focus()  
    
    # Validate IP Address
    if(not validate_ip(ipaddress)):
        messagebox.showerror("Fail Message","Invalid IP Address!")  
    else:
        if(check_server_connection(ipaddress,int(port_number))):
            server_obj={'server_ip':ipaddress,'server_port':port_number} 
            if(client_server_service.update_serverInfo(server_obj)==None):     
                messagebox.showerror("Fail Message","Fail to Connect Server!")
        else:
             messagebox.showerror("Error Message","Your Server isn't Running!")            
    dialog.destroy()
    dialog.update()
    

def validate_ip(ip_address):
    # Regular expression to match a valid IPv4 address
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    
    if re.match(ip_pattern, ip_address):
        # Check if each octet is in the valid range (0-255)
        if all(0 <= int(octet) <= 255 for octet in ip_address.split(".")):
            return True
    return False

           
        
        

      
    
       
    
    