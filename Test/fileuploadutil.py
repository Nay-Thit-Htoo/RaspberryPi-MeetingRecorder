import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import shutil

class FileUploaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Uploader")
        self.geometry("400x200")

        # Upload Button
        self.upload_button = tk.Button(self, text="Select and Upload File", command=self.select_file)
        self.upload_button.pack(pady=20)

        # Progress Bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)

        # Label to show upload percentage
        self.progress_label = tk.Label(self, text="Upload Progress: 0%")
        self.progress_label.pack()

        # Placeholder for file path
        self.filepath = None

    def select_file(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath:
            # Replace with your network folder path
            network_folder = r"\\ZINMIN-1281999\PythonProject\RecordFile"
            filename = os.path.basename(self.filepath)
            dest_path = os.path.join(network_folder, filename)

            # Start the upload process
            self.upload_file(self.filepath, dest_path)

    def upload_file(self, source_path, dest_path):
        file_size = os.path.getsize(source_path)
        chunk_size = 1024 * 1024  # 1 MB per chunk
        uploaded = 0

        try:
            with open(source_path, 'rb') as src, open(dest_path, 'wb') as dst:
                while True:
                    chunk = src.read(chunk_size)
                    if not chunk:
                        break
                    dst.write(chunk)
                    uploaded += len(chunk)

                    # Update progress bar and label
                    percent = int((uploaded / file_size) * 100)
                    self.progress['value'] = percent
                    self.progress_label.config(text=f"Upload Progress: {percent}%")
                    self.update_idletasks()  # Update the GUI during the process

            messagebox.showinfo("Success", "File uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload the file.\n{str(e)}")

if __name__ == "__main__":
    app = FileUploaderApp()
    app.mainloop()
