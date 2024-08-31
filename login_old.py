import tkinter as tk
import tkinter.font as tkFont
import client_services as clientservice
import socket

def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the geometry of the window
    window.geometry(f'{width}x{height}+{x}+{y}')


def login():
    username = username_entry.get()
    password = password_entry.get()
    if(not username):
        return username_entry.focus()
    if(not password):
        return password_entry.focus()   
    
    clientservice.client_login({'username':username,'password':password,'ipaddress':str(socket.gethostbyname(socket.gethostname()))})
         


# Set the window size
window_width = 400
window_height = 300

root = tk.Tk()
root.title("Login")

# Font Style
title_font=tkFont.Font(family="Helvetica", size=16, weight="bold")
label_font=tkFont.Font(family="Helvetica", size=12)

# Create a frame to hold the widgets
login_frame = tk.Frame(root)
login_frame.pack(padx=10, pady=5,expand=True)

# Title 
title_label = tk.Label(login_frame, text='Meeting Recorder',font=title_font)
title_label.pack(pady=20)

# Username label and entry
username_label = tk.Label(login_frame, text="Username:",font=label_font)
username_label.pack(padx=5, pady=5, anchor='w')
username_entry = tk.Entry(login_frame,font=label_font)
username_entry.pack(padx=5, pady=5)

# Password label and entry
password_label = tk.Label(login_frame, text="Password:",font=label_font)
password_label.pack(padx=5, pady=5, anchor='w')
password_entry = tk.Entry(login_frame, show="*",font=label_font)
password_entry.pack(padx=5, pady=5)

# Login button
login_button =tk.Button(login_frame,text="Login",bg="#121212", fg="white",width=15,height=1,font=label_font,command=login)
login_button.pack(padx=5, pady=15)

# Center the window
center_window(root, window_width, window_height)

root.mainloop()