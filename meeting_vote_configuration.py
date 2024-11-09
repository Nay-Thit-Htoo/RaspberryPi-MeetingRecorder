import os
import tkinter as tk
import tkinter.font as tkFont
from datetime import datetime

import meeting_vote_service

class MeetingVoteConfiguration:
    def __init__(self, parent_app):  
        self.parent_app=parent_app        

        title_font=tkFont.Font(family="Helvetica", size=14, weight="bold")
        label_font=tkFont.Font(family="Helvetica", size=11) 
        button_font=tkFont.Font(family="Helvetica", size=12)            
      
        width=420
        height=200 
        screen_width = self.parent_app.winfo_screenwidth()
        screen_height = self.parent_app.winfo_screenheight()

        # Calculate the position to center the window
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)     
        
        self.dialog = tk.Toplevel(parent_app)
        self.dialog.title("Meeting Vote Configuration")           
        # dialog.iconbitmap('Assets/recording-icon.ico')
        self.dialog.geometry(f'{width}x{height}+{x}+{y}') # Set the geometry of the window   
   
        # Create a frame to hold the widgets
        frame = tk.Frame( self.dialog)
        frame.pack(expand=True)

        # Title 
        title_label = tk.Label(frame, text='Meeting Vote',font=title_font)
        title_label.grid(row=0,column=0,pady=20,columnspan=2)
             
        # Meeting Title label and entry
        meeting_title_label = tk.Label(frame, text="Title",font=label_font)
        meeting_title_label.grid(row=1,column=0,padx=5, pady=5)
        self.meeting_title_entry = tk.Entry(frame,font=label_font,width=30)
        self.meeting_title_entry.grid(row=1,column=1,padx=5, pady=5)          
       
        # Start Vote button
        start_vote_button =tk.Button(frame,text="Start Vote",bg="#121212", fg="white",width=15,height=1,font=button_font,command=self.start_vote)
        start_vote_button.grid(row=2,column=0,pady=15,columnspan=3)  
                
    def start_vote(self):
        meeting_title = self.meeting_title_entry.get()      
        if(not meeting_title):
            return self.meeting_title_entry.focus()             
        meeting_vote_service.add_new_meeting_vote(meeting_title)
        self.parent_app.show_meeting_vote_info(meeting_title)
        self.dialog.destroy()
        self.dialog.update()
    
    def write_logtext(self,log_text):
          logDate=f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
          self.parent_app.logs_txt.insert(tk.END,f"[{logDate}]{log_text}\n")  
 