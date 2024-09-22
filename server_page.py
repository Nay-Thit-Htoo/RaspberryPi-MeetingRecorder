import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
from PIL import Image, ImageTk
from Settings import server_service
from reset_server_configuration import ResetServerConfiguration
import server_socket

class ServerPage(tk.Tk):
    def __init__(self,): 
        super().__init__()
        self.server_setting_info=server_service.read_setting_data()  

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

        # Server Port Number
        server_port_number_label = tk.Label(frame,text='Server Port : ',font=label_font)
        server_port_number_label.grid(row=2,column=0,pady=5)
        
        server_port_number_txt = tk.Label(frame,text=self.server_setting_info['port_number'],font=label_font)
        server_port_number_txt.grid(row=2,column=1,pady=5)

        # Server Audio Store File Path
        audio_store_file_label = tk.Label(frame,text='Audio Store File Path : ', font=label_font)
        audio_store_file_label.grid(row=3,column=0,pady=5)
        
        audio_store_file_txt = tk.Label(frame,text=self.server_setting_info['upload_file_path'],font=label_font)
        audio_store_file_txt.grid(row=3,column=1,pady=5)
       
        # Save & Start button
        self.save_start_btn =tk.Button(frame,text="Start",bg="#121212", fg="white",width=15,height=1,font=label_font)                                
        self.save_start_btn.grid(row=4,column=0,pady=15,columnspan=2)        
      
        # Reset Configuration
        reset_server_label = tk.Label(frame, text="Reset Configuration?",font=label_sm_font,fg="blue",cursor="hand2")
        reset_server_label.grid(row=5,column=0,padx=5, pady=2,columnspan=3)
        reset_server_label.bind("<Button-1>", self.on_label_click)

       
    def on_label_click(self,event):
        ResetServerConfiguration(self)

    def start_server(self):
        if(self.server_setting_info is None or self.server_setting_info['port_number'] is None or self.server_setting_info['upload_file_path']):
            ResetServerConfiguration(self)
        else:
            server_socket.start_server(int(self.server_setting_info['port_number']))              
 

if __name__ == "__main__":
    app = ServerPage()
    app.mainloop()

      