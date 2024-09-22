import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def choose_folder_and_share():
    # Open folder dialog to choose a directory
    folder_path = filedialog.askdirectory()
    
    if folder_path:
        # Folder name for the network share
        share_name = os.path.basename(folder_path)
        
        # Prepare the command to share the folder
        command = f'net share {share_name}="{folder_path}" /GRANT:everyone,full'
        
        try:
            # Run the net share command using subprocess
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            # Check the result of the command
            if result.returncode == 0:
                print(f'Successfully shared {folder_path} as {share_name}')
            else:
                print(f'Error: {result.stderr}')
        except Exception as e:
            print(f"An error occurred: {e}")

# Create the main Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Call the function to choose folder and share
choose_folder_and_share()
