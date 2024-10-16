import os
import socket
import threading
import tkinter as tk
from tkinter import Canvas, PhotoImage, messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
from Settings import server_service
from reset_server_configuration import ResetServerConfiguration
from server_socket import ServerSocket
from tkinter import scrolledtext
from datetime import datetime


class ServerPage(tk.Tk):
    def __init__(self): 
        super().__init__()
        self.server_setting_info=server_service.read_setting_data()  
        self.server_socket=None

        title_font=tkFont.Font(family="Helvetica", size=13, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=10)  
        label_sm_font=tkFont.Font(family="Helvetica", size=9)   

        self.title("Meeting Record (Server)")
        self.image = Image.open("Assets/icon.png")
        self.icon = ImageTk.PhotoImage(self.image)    
        self.iconphoto(True,self.icon)   

        width=600
        height=400        
        # Get the screen width and height        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

         # Calculate the position to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window
        self.geometry(f'{width}x{height}+{x}+{y}')     
       
        
        # Load the image
        self.original_image = Image.open("Assets/background.jpg")

        # Create a label to display the background image
        self.background_label = tk.Label(self)
        self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        frame = tk.Frame(self)
        frame.pack(expand=True)
      
        # control frame
        control_frame = tk.Frame(frame)
        control_frame.pack(anchor='center',padx=20,pady=20)

        # Title 
        title_label = tk.Label(control_frame, text='Meeting Record ( Server )',font=title_font)
        title_label.grid(row=0,column=0,pady=5,columnspan=2)

        # Server IP Address 
        server_ip_address_label = tk.Label(control_frame,text='Server IP : ',font=label_font)
        server_ip_address_label.grid(row=1,column=0,pady=5)

        server_ip_address_txt = tk.Label(control_frame,font=label_font)
        server_ip_address_txt.grid(row=1,column=1,pady=5)
        server_ip_address_txt.config(text=socket.gethostbyname(socket.gethostname()))

        # Server Port Number
        server_port_number_label = tk.Label(control_frame,text='Server Port : ',font=label_font)
        server_port_number_label.grid(row=2,column=0,pady=5)
        
        self.server_port_number_txt = tk.Label(control_frame,text=self.server_setting_info['port_number'],font=label_font)
        self.server_port_number_txt.grid(row=2,column=1,pady=5)        

        # Server Audio Store File Path
        audio_store_file_label = tk.Label(control_frame,text='Audio Store File Path : ', font=label_font)
        audio_store_file_label.grid(row=3,column=0,pady=5)
        
        self.audio_store_file_txt = tk.Label(control_frame,text=self.server_setting_info['upload_file_path'],font=label_font)
        self.audio_store_file_txt.grid(row=3,column=1,pady=5)
       
        # Start button
        self.server_start_btn =tk.Button(control_frame,text="Start",bg="#121212", fg="white",width=15,height=1,font=label_font,command=self.start_server)                                
        self.server_start_btn.grid(row=4,column=0,pady=15)  
            
        # Stop button
        self.server_stop_btn =tk.Button(control_frame,text="Stop",bg="#121212", fg="white",width=15,height=1,font=label_font,command=self.stop_server)                                
        self.server_stop_btn.grid(row=4,column=1,pady=15) 
        self.server_stop_btn.config(state='disabled')
      
        # Reset Configuration
        reset_server_label = tk.Label(control_frame, text="Reset Configuration?",font=label_sm_font,fg="blue",cursor="hand2")
        reset_server_label.grid(row=5,column=0,padx=5, pady=2,columnspan=2)
        reset_server_label.bind("<Button-1>", self.on_label_click)

        # View Log
        self.logs_txt = scrolledtext.ScrolledText(frame, wrap=tk.WORD,bg="black",fg="white",width=screen_width)
        self.logs_txt.pack()
        self.logs_txt.pack_forget()   

        # Bind the window resizing event
        self.bind("<Configure>", self.resize_background)

    def resize_background(self, event=None):
        # Get the current window dimensions
        width = self.winfo_width()
        height = self.winfo_height()

        # Resize the image to fit the current window size
        resized_image = self.original_image.resize((width, height), Image.Resampling.LANCZOS)

        # Convert the resized image to ImageTk format
        self.tk_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the new image
        self.background_label.config(image=self.tk_image)    

    # Reset Server Configuration Label Click   
    def on_label_click(self,event):
        ResetServerConfiguration(self)

    def start_server(self):
        self.server_setting_info=server_service.read_setting_data()  
        start_btn_txt=self.server_start_btn.cget("text")
        print(f'[Server info] : {self.server_setting_info}')
        if(start_btn_txt.lower()!="running"):
            self.logs_txt.pack()  
            if(self.server_setting_info is None or self.server_setting_info['port_number'] is None or self.server_setting_info['upload_file_path'] is None):
                ResetServerConfiguration(self)
            elif(not self.check_world_writable(self.server_setting_info['upload_file_path'])):                
                messagebox.showerror("File Permission",f"{self.server_setting_info['upload_file_path']} don't have Write Permission!")
            else:
                self.server_start_btn.config(text="Running"),
                self.server_start_btn.config(state='disabled')
                self.server_stop_btn.config(state='normal')

                call_server_socket_thread=threading.Thread(target=self.call_server_socket)
                call_server_socket_thread.start()
             
    def stop_server(self):   
        self.server_start_btn.config(text="Start")
        self.server_start_btn.config(state='normal')
        self.server_socket.stop_server(self.logs_txt)  

    def call_server_socket(self):
        self.server_socket=ServerSocket(port=int(self.server_setting_info['port_number']))
        self.server_socket.start_server(self.logs_txt)  
    
    def write_logtext(self,log_text):
        logDate=f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        self.logs_txt.insert(tk.END,f"[{logDate}]{log_text}\n")

    def check_world_writable(self,file_path):       
        self.write_logtext(f"[Server Page] [Check Folder Writeable]: {file_path}")
        print(f"[Server Page] [Check Folder Writeable]: {file_path}")
        test_file = os.path.join(file_path, "test_write.txt")
        try:
            # Try writing a test file
            with open(test_file, "w") as file:
                file.write("This is a test to check if the folder is writable.")
             # Optionally, clean up by removing the test file
            os.remove(test_file)
            self.write_logtext(f"[Server Page] [Check Folder Writeable]: {file_path} can write!")
            print(f"[Server Page] [Check Folder Writeable]: {file_path} can write!")
            return True
        except Exception as e:
            self.write_logtext(f"[Server Page] [Check Folder Writeable]: {e}")
            print(f"[Server Page] [Check Folder Writeable]: {e}")
            return False

if __name__ == "__main__":
    app = ServerPage()
    app.mainloop()