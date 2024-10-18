import tkinter as tk
from PIL import Image, ImageTk
from login import Login 
from meeting_record import MeetingRecord
import tkinter.font as tkFont

class Main(tk.Tk):
    def __init__(self,):
        super().__init__()
        self.title("Recorder Project")
        # Font Style for Label
        self.label_font=tkFont.Font(family="Helvetica", size=10)   

        self.image = Image.open("Assets/icon.png")
        self.icon = ImageTk.PhotoImage(self.image)    
        self.iconphoto(True,self.icon)

        self.start_meeting_button =tk.Button(self,text="Start Meeting",bg="#2185D5", fg="white",width=14,height=1,font=self.label_font,command=self.start_meeting_button_click)  
        self.stop_meeting_button =tk.Button(self,text="Stop Meeting",bg="#50717B", fg="white",width=14,height=1,font=self.label_font,command=self.stop_meeting_button_click)  

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
    
        # Create a container for the frames
        self.container = tk.Frame(self,bg="lightgreen")
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

    def show_frame(self, page_name):
        self.frame = self.frames[page_name]        
        self.frame.tkraise()    

        if hasattr(self.frame, "on_show"):
         self.frame.on_show()
    
    def show_meeting_buttons(self):    
        self.start_meeting_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)  

    def start_meeting_button_click(self):   
        self.start_meeting_button.place_forget() 
        self.stop_meeting_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)
        if hasattr(self.frame, "start_meeting"):           
           self.frame.start_meeting()

    def stop_meeting_button_click(self):   
        self.stop_meeting_button.place_forget() 
        self.start_meeting_button.place(relx=1.0, rely=0.0, anchor='ne', x=-10, y=10)  
        if hasattr(self.frame, "stop_meeting"):          
           self.frame.stop_meeting()

    def change_window_title(self,titleName):
        self.title(titleName)

if __name__ == "__main__":
    app = Main()
    app.mainloop()