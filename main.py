import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from login import Login 
import tkinter.font as tkFont
import client_server_service as clientservice
from meeting_record import MeetingRecord
from meeting_record_chairman import MeetingRecordChairman 
import RPi.GPIO as GPIO # type: ignore

class Main(tk.Tk):
    def __init__(self,):
        super().__init__()
        self.title("Recorder Project") 
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(32, GPIO.OUT)  # GPIO 18 as output     
        GPIO.cleanup()


        # Font Style for Label
        self.label_font=tkFont.Font(family="Helvetica", size=12)
        self.button_font=tkFont.Font(family="Helvetica", size=12)
        self.logged_user_info=clientservice.read_clientInfo()   

        # Get the screen width and height        
        screen_width = self.winfo_screenwidth()
        screen_height=self.winfo_screenheight()

        self.geometry(f"{screen_width}x{screen_height}+0+0")  
  
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.image_path = os.path.join(self.script_dir, "Assets", "icon.png")
        self.image = Image.open(self.image_path)
        self.icon = ImageTk.PhotoImage(self.image)    
        self.iconphoto(True,self.icon)        

        self.change_background_button =tk.Button(self,text="Change Background",bg="#006989", fg="white",width=16,height=1,font=self.button_font,command=self.change_background_image)  
        self.start_meeting_button =tk.Button(self,text="Start Meeting",bg="#2185D5", fg="white",width=14,height=1,font=self.button_font,command=self.start_meeting_button_click)  
        self.stop_meeting_button =tk.Button(self,text="Stop Meeting",bg="#50717B", fg="white",width=14,height=1,font=self.button_font,command=self.stop_meeting_button_click)  
        
        self.original_image_path = os.path.join(self.script_dir,self.logged_user_info["background_image"])
        self.original_image = Image.open(self.original_image_path)

        # Create a label to display the background image
        self.background_label = tk.Label(self)
        self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create a container for the frames
        self.container = tk.Frame(self)
        self.container.pack(expand=True)        
             
        # Create the frames for each page
        self.frames = {}       
        self.frame=""
        for F in (Login,MeetingRecord, MeetingRecordChairman):
            page_name = F.__name__
            self.frame = F(parent=self.container, controller=self)
            self.frames[page_name] = self.frame           
            self.frame.grid(row=0, column=0, sticky="nsew")         

        # Show the first page
        self.show_frame("Login")     
        
        # Bind the window resizing event
        self.bind("<Configure>", self.resize_background)
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy()
        if(self.frame.__class__.__name__=="MeetingRecordChairman"):
            if hasattr(self.frame, "close_window_chairman"):           
             self.frame.close_window_chairman()
        elif(self.frame.__class__.__name__=="MeetingRecord"):
            if hasattr(self.frame, "close_window_client"):           
             self.frame.close_window_client()

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
  
    def show_frame(self, page_name):
        self.frame = self.frames[page_name]        
        self.frame.tkraise()    

        if hasattr(self.frame, "on_show"):
         self.frame.on_show()
    
    def show_meeting_buttons(self):            
        self.start_meeting_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.start_meeting_button.tkraise()

    def show_change_background_btn(self):
        self.change_background_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.change_background_button.tkraise()

    def start_meeting_button_click(self):   
        self.start_meeting_button.place_forget() 
        self.stop_meeting_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.stop_meeting_button.tkraise()
        if hasattr(self.frame, "start_meeting_chairman"):           
           self.frame.start_meeting_chairman()

    def stop_meeting_button_click(self):
        self.stop_meeting_button.place_forget() 
        self.start_meeting_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.start_meeting_button.tkraise()  
        if hasattr(self.frame, "stop_meeting_chairman"):          
           self.frame.stop_meeting_chairman()        
    
    def hide_change_background_btn(self):
         print(f"Reach Change Background Btn Hide")
         self.change_background_button.place_forget()

    def change_window_title(self,titleName):
        self.title(titleName)
    
    def change_background_image(self):
        file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
        )
        if file_path:         
          print(f"Update Image Path:{file_path}")
          clientservice.update_background_image(file_path)
          self.original_image=Image.open(file_path)      
          self.resize_background()
    
if __name__ == "__main__":
    app = Main()
    app.mainloop()