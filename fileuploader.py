import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tqdm import tqdm
import threading

class FileUploader(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("File Uploader")
        self.geometry("400x200")
        
        self.label = tk.Label(self, text="Select a file to upload")
        self.label.pack(pady=10)
        
        self.browse_button = tk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=10)
        
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=10)
        
        self.upload_button = tk.Button(self, text="Upload", command=self.upload_file)
        self.upload_button.pack(pady=10)
        
        self.file_path = None
        self.network_path = "\\ZINMIN-1281999\PythonProject\RecordFile"  # Change this to your network share path

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.label.config(text=self.file_path)
    
    def upload_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return
        
        threading.Thread(target=self.upload_file_thread).start()    

    
    def upload_file_thread(self):
        file_name = os.path.basename(self.file_path)
        dest_path = os.path.join(self.network_path, file_name)
        
        file_size = os.path.getsize(self.file_path)
        self.progress["maximum"] = file_size
        
        with open(self.file_path, 'rb') as src_file:
            with open(dest_path, 'wb') as dest_file:
                while True:
                    # Read the file in chunks (64KB)
                    chunk = src_file.read(1024)
                    if not chunk:
                        break
                    dest_file.write(chunk)                   
                    self.progress.step(len(chunk)) 
                    
        messagebox.showinfo("Success", "File uploaded successfully!")

if __name__ == "__main__":
    app = FileUploader()
    app.mainloop()
