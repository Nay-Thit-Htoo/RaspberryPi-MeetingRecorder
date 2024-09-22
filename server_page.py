import socket
import threading
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
from Settings import server_service
from reset_server_configuration import ResetServerConfiguration
from server_socket import ServerSocket


class ServerPage(tk.Tk):
    def __init__(self,): 
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

        width=500
        height=300        
        # Get the screen width and height        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

         # Calculate the position to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window
        self.geometry(f'{width}x{height}+{x}+{y}')
        frame = tk.Frame(self)
        frame.pack(expand=True)
      
        # Title 
        title_label = tk.Label(frame, text='Meeting Record ( Server )',font=title_font)
        title_label.grid(row=0,column=0,pady=5,columnspan=3)

        # Server IP Address 
        server_ip_address_label = tk.Label(frame,text='Server IP : ',font=label_font)
        server_ip_address_label.grid(row=1,column=0,pady=5)

        server_ip_address_txt = tk.Label(frame,font=label_font)
        server_ip_address_txt.grid(row=1,column=1,pady=5)
        server_ip_address_txt.config(text=socket.gethostbyname(socket.gethostname()))

        # Server Port Number
        server_port_number_label = tk.Label(frame,text='Server Port : ',font=label_font)
        server_port_number_label.grid(row=2,column=0,pady=5)
        
        self.server_port_number_txt = tk.Label(frame,text=self.server_setting_info['port_number'],font=label_font)
        self.server_port_number_txt.grid(row=2,column=1,pady=5)        

        # Server Audio Store File Path
        audio_store_file_label = tk.Label(frame,text='Audio Store File Path : ', font=label_font)
        audio_store_file_label.grid(row=3,column=0,pady=5)
        
        self.audio_store_file_txt = tk.Label(frame,text=self.server_setting_info['upload_file_path'],font=label_font)
        self.audio_store_file_txt.grid(row=3,column=1,pady=5)
       
        # Start button
        self.server_start_btn =tk.Button(frame,text="Start",bg="#121212", fg="white",width=15,height=1,font=label_font,command=self.start_server)                                
        self.server_start_btn.grid(row=4,column=0,pady=15)  
            
        # Stop button
        self.server_stop_btn =tk.Button(frame,text="Stop",bg="#121212", fg="white",width=15,height=1,font=label_font,command=self.stop_server)                                
        self.server_stop_btn.grid(row=4,column=1,pady=15) 
        self.server_stop_btn.config(state='disabled')
      
        # Reset Configuration
        reset_server_label = tk.Label(frame, text="Reset Configuration?",font=label_sm_font,fg="blue",cursor="hand2")
        reset_server_label.grid(row=5,column=0,padx=5, pady=2,columnspan=3)
        reset_server_label.bind("<Button-1>", self.on_label_click)
       
    def on_label_click(self,event):
        ResetServerConfiguration(self)

    def start_server(self):
        start_btn_txt=self.server_start_btn.cget("text")
        print(f'server info: {self.server_setting_info}')
        if(start_btn_txt.lower()!="running"):
            if(self.server_setting_info is None or self.server_setting_info['port_number'] is None or self.server_setting_info['upload_file_path'] is None):
                ResetServerConfiguration(self)
            else:
                self.server_start_btn.config(text="Running"),
                self.server_start_btn.config(state='disabled')
                self.server_stop_btn.config(state='normal')

                call_server_socket_thread=threading.Thread(target=self.call_server_socket)
                call_server_socket_thread.start()
             
    def stop_server(self):   
        self.server_start_btn.config(text="Start")
        self.server_start_btn.config(state='normal')
        self.server_socket.stop_server()  

    def call_server_socket(self):
        self.server_socket=ServerSocket(port=int(self.server_setting_info['port_number']))
        self.server_socket.start_server()  


if __name__ == "__main__":
    app = ServerPage()
    app.mainloop()