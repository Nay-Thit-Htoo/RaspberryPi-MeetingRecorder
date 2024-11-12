import os
import subprocess

def create_and_copy_to_network_share(local_folder, remote_folder, server_address, share_name, username, password):
    # Check if the local folder exists
    if not os.path.exists(local_folder):
        print("Local folder does not exist.")
        return

    # Step 1: Create the target folder on the Windows network share
    create_folder_command = [
        "smbclient", f"//{server_address}/{share_name}", "-U", f"{username}%{password}", "-c",
        f'mkdir "{remote_folder}"'
    ]
    
    try:
        subprocess.run(create_folder_command, check=True, capture_output=True, text=True)
        print(f"Created folder '{remote_folder}' on network share.")
    except subprocess.CalledProcessError as e:
        print("Error creating remote folder:", e.stderr)
        return

    # Step 2: Copy files from local folder to the network share
    copy_command = [
        "smbclient", f"//{server_address}/{share_name}", "-U", f"{username}%{password}", "-c",
        f'lcd "{local_folder}"; cd "{remote_folder}"; prompt OFF; recurse ON; mput *'
    ]
    
    try:
        subprocess.run(copy_command, check=True, capture_output=True, text=True)
        print("Files copied successfully to network share.")
    except subprocess.CalledProcessError as e:
        print("Error copying files:", e.stderr)

# Usage
local_folder = "/home/alpha/Desktop/Test"  # Local folder path on your Raspberry Pi
remote_folder = "NTH"      # Folder to create on network share
server_address = "192.168.43.157"         # IP address of the Windows machine
share_name = "NTHShare"                # Name of the Windows share
username = "abank\\naythithtoo"              # Username for network share
password = "Galanthus123!@#"              # Password for network share

create_and_copy_to_network_share(local_folder, remote_folder, server_address, share_name, username, password)
