import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from login import Login 
from meeting_record import MeetingRecord
import tkinter.font as tkFont
import client_server_service as clientservice
import RPi.GPIO as GPIO # type: ignore

class Main(tk.Tk):
    def __init__(self,):
        super().__init__()
        self.title("Recorder Project")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(32, GPIO.OUT)  # GPIO 18 as output    

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

        self.recording_user_frame =self.create_recording_user_frame() 
        

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
        #hide recording user list frame & remove all recording users
        self.recording_frame_hide_remove_children()
        self.stop_meeting_button.place_forget() 
        self.start_meeting_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        self.start_meeting_button.tkraise()  
        if hasattr(self.frame, "stop_meeting"):          
           self.frame.stop_meeting()
        self.remove_recording_user()
    
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

    def create_recording_user_frame(root):
        root.right_margin = 40
        # Create a main frame
        root.record_user_main_frame =  tk.Frame(root,bg="#424242")
        root.record_user_main_frame.place(relx=1.0, rely=0.5, anchor="e",relheight=0.7,x=-root.right_margin)
        root.record_user_main_frame.place_forget()

        # Create a canvas
        canvas = tk.Canvas(root.record_user_main_frame,width=210,background="#424242")
        canvas.pack(side="left", fill="both", expand=True)

        # Add a scrollbar to the canvas
        scrollbar = tk.Scrollbar(root.record_user_main_frame, orient="vertical", command=canvas.yview,background="#424242")
        scrollbar.pack(side="right", fill="y")

        # Configure the canvas to work with the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas
        scrollable_frame = tk.Frame(canvas)

        # Add the frame to the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        root.auto_scroll(canvas)
        return scrollable_frame

    def auto_scroll(self,canvas):
        canvas.yview_scroll(1, "units")  # Scroll by 1 unit

    def create_recording_users(self,clients):
        for client in clients:
            self.blc_user_frame=tk.Frame(self.recording_user_frame)
            self.blc_user_frame.pack(pady=(5,10))

            self.recorder_name_label = tk.Label(self.blc_user_frame, text=client["usercode"],width=14)
            self.recorder_name_label.grid(row=0, column=0, padx=10)

            
            self.remove_btn = tk.Button(self.blc_user_frame, text=f"Remove",bg="#E90074",fg="#FFFFFF",command=lambda: self.remove_recording_user(clients,client))
            self.remove_btn.grid(row=0, column=1,padx=10)
  
    def show_recording_user_frame(self,clients):
        print(f"[Meeting Record][Recording Users] : {clients[0]}")  
        self.record_user_main_frame.place(relx=1.0, rely=0.5, anchor="e",relheight=0.7,x=-self.right_margin)              
        self.recorder_header_label = tk.Label(self.recording_user_frame, text=f"Clients",width=20,bg="#229799",fg='#FFFFFF',font=("Arial", 14),height=2)
        self.recorder_header_label.pack(padx=(2,0)) 
        self.create_recording_users(clients)

    def remove_recording_user(self,clients,clientObj):
        if hasattr(self.frame, "remove_recording_client"):           
           self.frame.remove_recording_client(clientObj)
        for widget in self.recording_user_frame.winfo_children():
            widget.destroy()
        new_clients = list(filter(lambda p: p!=clientObj, clients))
        if len(new_clients)==0:
          self.recording_frame_hide_remove_children()
        else:
          self.show_recording_user_frame(new_clients)

    def recording_frame_hide_remove_children(self):
        self.record_user_main_frame.place_forget()
        for widget in self.recording_user_frame.winfo_children():
            widget.destroy()
    GPIO.cleanup()
if __name__ == "__main__":
    app = Main()
    app.mainloop()