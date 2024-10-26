import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from login import Login 
from meeting_record import MeetingRecord
import tkinter.font as tkFont
import client_server_service as clientservice

class Main(tk.Tk):
    def __init__(self,):
        super().__init__()
        self.title("Recorder Project")
        # Font Style for Label
        self.label_font=tkFont.Font(family="Helvetica", size=12)
        self.button_font=tkFont.Font(family="Helvetica", size=12)
        self.logged_user_info=clientservice.read_clientInfo()   

        self.image = Image.open("Assets/icon.png")
        self.icon = ImageTk.PhotoImage(self.image)    
        self.iconphoto(True,self.icon)

        self.change_background_button =tk.Button(self,text="Change Background",bg="#006989", fg="white",width=16,height=1,font=self.button_font,command=self.change_background_image)  
        self.start_meeting_button =tk.Button(self,text="Start Meeting",bg="#2185D5", fg="white",width=14,height=1,font=self.button_font,command=self.start_meeting_button_click)  
        self.stop_meeting_button =tk.Button(self,text="Stop Meeting",bg="#50717B", fg="white",width=14,height=1,font=self.button_font,command=self.stop_meeting_button_click)  

        width=600
        height=300        
        # Get the screen width and height        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

         # Calculate the position to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window
        self.geometry(f'{width}x{height}+{x}+{y}')   

        self.original_image = Image.open(self.logged_user_info["background_image"])

        # Create a label to display the background image
        self.background_label = tk.Label(self)
        self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1)            
    
        # Create a container for the frames
        self.container = tk.Frame(self)
        self.container.pack(expand=True)        
             
        # Create the frames for each page
        self.frames = {}       
        self.frame=""
        for F in (Login, MeetingRecord):
            page_name = F.__name__
            self.frame = F(parent=self.container, controller=self)
            self.frames[page_name] = self.frame           
            self.frame.grid(row=0, column=0, sticky="nsew")         

        # Show the first page
        self.show_frame("Login")     
        
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
        if hasattr(self.frame, "start_meeting"):           
           self.frame.start_meeting()

    def stop_meeting_button_click(self):   
        self.stop_meeting_button.place_forget() 
        self.start_meeting_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.start_meeting_button.tkraise()  
        if hasattr(self.frame, "stop_meeting"):          
           self.frame.stop_meeting()
    
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