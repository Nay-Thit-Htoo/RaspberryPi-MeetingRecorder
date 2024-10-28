import os
import subprocess

# Configuration
local_folder = "/path/to/local/folder"
remote_share = "//192.168.43.157/NTHShare"
username = "abank\naythithtoo"
password = "Galanthus123!@#"

def copy_folder_to_share(local_folder, remote_share, username, password):
    # Iterate over all files in the local folder
    for root, dirs, files in os.walk(local_folder):
        for file_name in files:
            # Define the full local path
            local_file = os.path.join(root, file_name)
            
            # Define the remote path within the network share
            remote_path = os.path.relpath(local_file, local_folder).replace(os.sep, "/")
            
            # Command to copy file using smbclient
            smbclient_command = [
                "smbclient", remote_share, "-U", username, "-c",
                f'put "{local_file}" "{remote_path}"'
            ]
            
            # Run smbclient command
            try:
                result = subprocess.run(
                    smbclient_command, input=password, text=True, capture_output=True, check=True
                )
                print(f"Copied {local_file} to {remote_share}/{remote_path}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to copy {local_file}: {e.stderr}")

# Execute folder copy
copy_folder_to_share(local_folder, remote_share, username, password)