import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
from Settings import server_service

class ResetServerConfiguration:
    def __init__(self, parent_app):  
        self.parent_app=parent_app     

        self.selected_audio_file_path = tk.StringVar()

        title_font=tkFont.Font(family="Helvetica", size=13, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=10)  
        label_sm_font=tkFont.Font(family="Helvetica", size=9)   
      
        width=400
        height=200 
        screen_width = self.parent_app.winfo_screenwidth()
        screen_height = self.parent_app.winfo_screenheight()

         # Calculate the position to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
     
        
        self.dialog = tk.Toplevel(parent_app)
        self.dialog.title("Reset Server Configuration")           
        # dialog.iconbitmap('Assets/recording-icon.ico')
        self.dialog.geometry(f'{width}x{height}+{x}+{y}') # Set the geometry of the window   

        # Register for Validate Key Press for only digit  
        validate_keypress=(self.dialog.register(self.validate_number_input), '%S')

        # Create a frame to hold the widgets
        frame = tk.Frame( self.dialog)
        frame.pack(expand=True)

        # Title 
        title_label = tk.Label(frame, text='Server Configuration',font=title_font)
        title_label.grid(row=0,column=0,pady=20,columnspan=3)
             
        # Port Number label and entry
        portnumber_label = tk.Label(frame, text="Port Number",font=label_font)
        portnumber_label.grid(row=1,column=0,padx=5, pady=5)
        self.portnumber_entry = tk.Entry(frame,font=label_font,validate='key',width=30,validatecommand=validate_keypress)
        self.portnumber_entry.grid(row=1,column=1,padx=5, pady=5,columnspan=2)

        # Audio Store File Path label and entry
        audio_studio_file_path_label = tk.Label(frame, text="Audio Store File Path",font=label_font)
        audio_studio_file_path_label.grid(row=2,column=0,padx=5, pady=5)
        self.audio_studio_file_path_entry = tk.Entry(frame,font=label_font,textvariable=self.selected_audio_file_path)
        self.audio_studio_file_path_entry.grid(row=2,column=1,padx=5, pady=5)
        self.audio_studio_file_path_entry.config(state='readonly')
    
        # File Choose
        file_choose_button =tk.Button(frame,text="Choose",bg="#0E46A3", fg="white",width=6,height=1,font=label_font,command=self.file_choose_btn_click)
        file_choose_button.grid(row=2,column=2,padx=5, pady=5)   

        # Login button
        save_button =tk.Button(frame,text="Save",bg="#121212", fg="white",width=15,height=1,font=label_font,command=self.save_server_configuration)
        save_button.grid(row=3,column=0,pady=15,columnspan=3)       

    def validate_number_input(self,char):
        # Allow only digits
        return char.isdigit() or char == ""

    def file_choose_btn_click(self):       
        self.selected_audio_file_path.set("")   
        folder_path=filedialog.askdirectory(title="Select a folder to save audio files!")
        if(folder_path):
            share_name = os.path.basename(folder_path)  
            self.selected_audio_file_path.set(f'\\\\{os.environ['COMPUTERNAME']}\\{share_name}')  

    def save_server_configuration(self):
        port_number = self.portnumber_entry.get()      
        if(not port_number):
            return self.portnumber_entry.focus()  
        elif 0 < int(port_number) > 65535:
             messagebox.showerror("Port Number Configuration",f"Port {port_number} exceeds the valid range.")
        
        audio_record_file_path = self.audio_studio_file_path_entry.get()      
        if(not audio_record_file_path):
            return self.audio_studio_file_path_entry.focus()
        else:
            audio_record_file_path=f"\\\\{audio_record_file_path.replace('/','\\')}"     
        
        server_service.update_server_info({
            "port_number": int(port_number),
            "upload_file_path": audio_record_file_path
        })         
        self.dialog.destroy()
        self.dialog.update()
    


           
        
        

      
    
       
    
    