import os
import shutil
import threading
import subprocess

def create_and_copy_to_network_share(local_folder, remote_folder, server_address, share_name, username, password):
    print(f"[File Upload To Server]:[Start Uploading...]")
    # Check if the local folder exists
    if not os.path.exists(local_folder):
        print(f"[File Upload To Server]: Local folder does not exist.")
        return
    
    local_folder=os.path.join(os.getcwd(), local_folder)
    # Step 1: Create the target folder on the Windows network share
    create_folder_command = [
        "smbclient", f"//{server_address}/{share_name}", "-U", f"{username}%{password}", "-c",
        f'mkdir "{remote_folder}"'
    ]
    print(f"[File Upload To Server]:[Server Address]:{server_address}")
    print(f"[File Upload To Server]:[Local Folder Name]:{local_folder}")
    print(f"[File Upload To Server]:[Remote Folder]:{remote_folder}")
    print(f"[File Upload To Server]:[Share Name]:{share_name}")
    print(f"[File Upload To Server]:[User Name]:{username}")
    print(f"[File Upload To Server]:[Password]:{password}")

    try:
        subprocess.run(create_folder_command, check=True, capture_output=True, text=True)
        print(f"[File Upload To Server]: Created folder '{remote_folder}' on network share.")
    except subprocess.CalledProcessError as e:
        print(f"[File Upload To Server]: Error creating remote folder:", e.stderr)
        return

    # Step 2: Copy files from local folder to the network share
    copy_command = [
        "smbclient", f"//{server_address}/{share_name}", "-U", f"{username}%{password}", "-c",
        f'lcd "{local_folder}"; cd "{remote_folder}"; prompt OFF; recurse ON; mput *'
    ]
    
    try:
        subprocess.run(copy_command, check=True, capture_output=True, text=True)
        print(f"[File Upload To Server]: Files copied successfully to network share.")
    except subprocess.CalledProcessError as e:
        print(f"[File Upload To Server]: Error copying files:", e.stderr)


def delete_file_after_upload(to_remove_file_path):
     print(f"[File Upload To Server]:[Remove Local File After Upload] {to_remove_file_path}")
     if os.path.exists(to_remove_file_path):
        if(os.path.isdir(to_remove_file_path)):
            os.rmdir(to_remove_file_path)
        else:
          os.remove(to_remove_file_path)
        print(f"[File Upload To Server]:[Successfully Remove Local File] {to_remove_file_path}") 

def file_upload_to_server(local_file_path,record_user_obj):
    local_file_path=os.path.join(os.getcwd(), local_file_path)
    remote_folder = record_user_obj['usercode']      # Folder to create on network share
    server_address = record_user_obj['server_ip']       # IP address of the Windows machine
    share_name = record_user_obj['server_share_folder_name']           # Name of the Windows share
    username =(record_user_obj['server_user_name']).replace("\\\\","\\")    # Username for network share
    password = record_user_obj['server_password']       
    file_upload_thread = threading.Thread(target=create_and_copy_to_network_share, args=(local_file_path,remote_folder,server_address, share_name, username, password))
    file_upload_thread.start()
    file_upload_thread.join()


# def upload_file_thread(local_file_path,record_user_obj):
#     print(f"[File Upload To Server]:[Start Uploading...]")
#     file_name = os.path.basename(local_file_path)
#     server_file_path=rf"{record_user_obj['upload_file_path']}"    
#     create_dest_folder_path = os.path.join(server_file_path,record_user_obj['usercode'])   
#     os.makedirs(create_dest_folder_path, exist_ok=True)  

#     to_upload_dest_path=os.path.join(create_dest_folder_path,file_name)
#     try:
#         # Copy the file to the network share
#         shutil.copy2(local_file_path, to_upload_dest_path)
#         print(f"[File Upload To Server]: [Successfully Uploaded...] {file_name}")        
#     except Exception as e:
#         print(f"[File Upload To Server]:[Failed to upload file: {str(e)}]") 
