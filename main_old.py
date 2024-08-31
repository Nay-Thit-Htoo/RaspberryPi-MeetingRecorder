import tkinter as tk

def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Set the geometry of the window
    window.geometry(f'{width}x{height}+{x}+{y}')

# Set the window size
window_width = 400
window_height = 300

root = tk.Tk()
root.title("Recorder Project")

# Create a frame to hold the widgets
frame = tk.Frame(root)
frame.pack(expand=True)

#region recorder image
image = tk.PhotoImage(file="Assets/mic.png")
label = tk.Label(frame, image=image)
label.pack(pady=10)

#start & stop buttons
startBtn=tk.Button(frame,text="Start",bg="#121212", fg="white",width=15,height=2,font=("Helvetica", 10))
stopBtn=tk.Button(frame,text="Stop",bg="#DEE3E2", fg="black",width=15,height=2,font=("Helvetica", 10))
startBtn.pack(side=tk.LEFT,padx=10, pady=10)
stopBtn.pack(side=tk.LEFT,padx=10, pady=10)

# Center the window
center_window(root, window_width, window_height)

root.mainloop()