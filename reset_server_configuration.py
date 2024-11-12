import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tkinter.font as tkFont
import server_service
from datetime import datetime

class ResetServerConfiguration:
    def __init__(self, parent_app):  
        self.parent_app=parent_app     

        self.selected_audio_file_path = tk.StringVar()
        self.os_user_name=tk.StringVar(value=self.get_full_username())
        self.share_folder_name=""

        title_font=tkFont.Font(family="Helvetica", size=14, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=11) 
        button_font=tkFont.Font(family="Helvetica", size=12)            
      
        width=420
        height=300 
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

         # Server User Name 
        username_label = tk.Label(frame, text="User Name",font=label_font)
        username_label.grid(row=2,column=0,padx=5, pady=5)
        self.username_entry = tk.Entry(frame,font=label_font,width=30,textvariable=self.os_user_name)
        self.username_entry.grid(row=2,column=1,padx=5, pady=5,columnspan=2)
        self.username_entry.config(state='readonly')

        # Server Password
        password_label = tk.Label(frame, text="Password",font=label_font)
        password_label.grid(row=3,column=0,padx=5, pady=5)
        self.password_entry = tk.Entry(frame,font=label_font,width=30)
        self.password_entry.grid(row=3,column=1,padx=5, pady=5,columnspan=2)

        # Audio Store File Path label and entry
        audio_studio_file_path_label = tk.Label(frame, text="Audio Store File Path",font=label_font)
        audio_studio_file_path_label.grid(row=4,column=0,padx=5, pady=5)
        self.audio_studio_file_path_entry = tk.Entry(frame,font=label_font,textvariable=self.selected_audio_file_path)
        self.audio_studio_file_path_entry.grid(row=4,column=1,padx=5, pady=5)
        self.audio_studio_file_path_entry.config(state='readonly')   
        
        # File Choose
        file_choose_button =tk.Button(frame,text="Choose",bg="#0E46A3", fg="white",width=6,height=1,font=button_font,command=self.file_choose_btn_click)
        file_choose_button.grid(row=4,column=2,padx=5, pady=5)   
       
        # Save button
        save_button =tk.Button(frame,text="Save",bg="#121212", fg="white",width=15,height=1,font=button_font,command=self.save_server_configuration)
        save_button.grid(row=5,column=0,pady=15,columnspan=3)  
            
    def get_full_username(self):
        try:
            org_full_username = rf'{subprocess.check_output("whoami", shell=True, text=True).strip()}'
            full_username=org_full_username.replace("\\","\\\\")
            return full_username
        except subprocess.CalledProcessError:
            return None

    def validate_number_input(self,char):
        # Allow only digits
        return char.isdigit() or char == ""

    def file_choose_btn_click(self):       
        self.selected_audio_file_path.set("")   
        self.dialog.attributes('-topmost', False)
        folder_path=filedialog.askdirectory(title="Select a folder to save audio files!")
        self.dialog.attributes('-topmost',True)
        if(folder_path):
            share_name = os.path.basename(folder_path) 
            command = f'net share {share_name}="{folder_path}" /grant:Everyone,full'        
            try:
                # Run the net share command using subprocess
                result = subprocess.run(command, shell=True, capture_output=True, text=True)                
                
                self.write_logtext(f"[Reset Server Configuration] [Result] : {result}")
                print(f"[Reset Server Configuration] [Result] : {result}")               

                # Check the result of the command
                if result.returncode == 0 or result.returncode == 2:
                    self.write_logtext(f"[Reset Server Configuration] Share Name : {share_name}")
                    print(f"[Reset Server Configuration] Share Name : {share_name}")
                    self.write_logtext(f"[Reset Server Configuration] : Successfully shared {folder_path} as {share_name}")
                    print(f'[Reset Server Configuration] : Successfully shared {folder_path} as {share_name}')                    
                    self.selected_audio_file_path.set(f"\\\\{os.environ['COMPUTERNAME']}\\{share_name}")
                    self.share_folder_name=share_name 
                else:
                    self.write_logtext(f"[Reset Server Configuration] [Error] : {result.stderr}\n")
                    print(f'[Reset Server Configuration] [Error] : {result.stderr}')
                    self.selected_audio_file_path.set("") 
            except Exception as e:                
                self.write_logtext(f"[Reset Server Configuration] [An error occurred] : {e}")
                print(f"[Reset Server Configuration] [File Choose Error] : {e}")
                self.selected_audio_file_path.set("")
            
    def save_server_configuration(self):
        port_number = self.portnumber_entry.get()      
        if(not port_number):
            return self.portnumber_entry.focus()
        else:
            port_number=int(port_number)
            if(port_number<1000 or port_number > 65535):
              self.dialog.attributes('-topmost', False)
              messagebox.showerror("Port Number Configuration",f"Port {port_number} length must be 4 at least and maximum range 65535.")
              self.dialog.attributes('-topmost', True)
              return
        
        audio_record_file_path = self.audio_studio_file_path_entry.get()      
        if(not audio_record_file_path):
            return self.audio_studio_file_path_entry.focus()   
        elif(not self.check_world_writable(audio_record_file_path)):
            self.dialog.attributes('-topmost', False)
            messagebox.showerror("File Permission",f"{audio_record_file_path} don't have Write Permission!")
            self.dialog.attributes('-topmost', True)  
            return self.audio_studio_file_path_entry.focus()    

        # Server user name entry
        server_user_name = self.username_entry.get()
        if(not server_user_name):
            return self.username_entry.focus()                 

        # Server user name entry
        server_user_password = self.password_entry.get()
        if(not server_user_password):
            return self.password_entry.focus()  

        server_service.update_server_info({
            "server_port_number": int(port_number),
            "server_share_folder_path":audio_record_file_path,
            "server_share_folder_name": self.share_folder_name,
            "server_user_name":server_user_name,
            "server_password":server_user_password
        })         
        # Change Server Page port Number and Audio Store File Path
        self.parent_app.audio_store_file_txt.config(text=audio_record_file_path)
        self.parent_app.server_port_number_txt.config(text=port_number)
        self.parent_app.server_user_name_txt.config(text=server_user_name)
        self.parent_app.server_user_password_txt.config(text=server_user_password)
        
        self.dialog.destroy()
        self.dialog.update()
    
    def write_logtext(self,log_text):
          logDate=f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
          self.parent_app.logs_txt.insert(tk.END,f"[{logDate}]{log_text}\n")
  
    def check_world_writable(self,file_path):      
        self.write_logtext(f"[Reset Server Configuration] [Check Folder Writeable]: {file_path}") 
        print(f"[Reset Server Configuration] [Check Folder Writeable]: {file_path}")
        test_file = os.path.join(file_path, "test_write.txt")
        try:
            # Try writing a test file
            with open(test_file, "w") as file:
                file.write("This is a test to check if the folder is writable.")
             # Optionally, clean up by removing the test file
            os.remove(test_file)
            self.write_logtext(f"[Reset Server Configuration] [Check Folder Writeable]: {file_path} can write!")
            print(f"[Reset Server Configuration] [Check Folder Writeable]: {file_path} can write!")
            return True
        except Exception as e:
           self.write_logtext(f"[Reset Server Configuration] [Check Folder Writeable]: {e}")
           print(f"[Reset Server Configuration] [Check Folder Writeable]: {e}")
           return False