import tkinter as tk
from login import Login 
from meeting_record import MeetingRecord

class Main(tk.Tk):
    def __init__(self,):
        super().__init__()
        self.title("Recorder Project")
        self.iconbitmap('Assets/recording-icon.ico')

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
        

        # Create a container for the frames
        self.container = tk.Frame(self)
        self.container.pack(expand=True)

        # Create the frames for each page
        self.frames = {}
        for F in (Login, MeetingRecord):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
    
        # Show the first page
        self.show_frame("Login")        

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()    
   
if __name__ == "__main__":
    app = Main()
    app.mainloop()