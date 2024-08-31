import tkinter as tk
from tkinter import messagebox

def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if username == 'user' and password == 'pass':  # Simple check
        messagebox.showinfo("Login", "Login successful")
    else:
        messagebox.showerror("Login", "Invalid username or password")

# Create the main window
root = tk.Tk()
root.title("Login Form")

# Create and place the widgets
tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Password").grid(row=1, column=0, padx=10, pady=10)

entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

tk.Button(root, text="Login", command=login).grid(row=2, column=1, padx=10, pady=10)

# Run the application
root.mainloop()
