import os
import shutil
import threading
import subprocess

def create_and_copy_to_network_share(local_folder, remote_folder, server_address, share_name, username, password):
    print(f"[File Upload To Server]:[Start Uploading...]")

    # Ensure local folder exists
    if not os.path.exists(local_folder):
        print(f"[File Upload To Server]: Local folder does not exist: {local_folder}")
        return

    local_folder = os.path.abspath(local_folder)  # Ensure absolute path

    # Logging (excluding password for security)
    print(f"[File Upload To Server]:[Server Address]: {server_address}")
    print(f"[File Upload To Server]:[Local Folder]: {local_folder}")
    print(f"[File Upload To Server]:[Remote Folder]: {remote_folder}")
    print(f"[File Upload To Server]:[Share Name]: {share_name}")
    print(f"[File Upload To Server]:[User Name]: {username}")

    # # Step 1: Create the target folder on the network share
    # create_folder_command = [
    #     "smbclient", f"//{server_address}/{share_name}", "-U", f"{username}%{password}",
    #     "--option=client min protocol=SMB2", "--option=client max protocol=SMB3",
    #     "-c", f'mkdir "{remote_folder}"'
    # ]

    # try:
    #     subprocess.run(create_folder_command, check=True, capture_output=True, text=True)
    #     print(f"[File Upload To Server]: Created folder '{remote_folder}' on network share.")
    # except subprocess.CalledProcessError as e:
    #     print(f"[File Upload To Server]: Error creating remote folder: {e.stderr}")
    #     return

    # Step 2: Copy files from local folder to the network share
    copy_command = [
        "smbclient", f"//{server_address}/{share_name}", "-U", f"{username}%{password}",
        "--option=client min protocol=SMB2", "--option=client max protocol=SMB3",
        "-c", f'lcd "{local_folder}"; cd "{remote_folder}"; prompt OFF; recurse ON; mput *'
    ]

    try:
        subprocess.run(copy_command, check=True, capture_output=True, text=True)
        print(f"[File Upload To Server]: Files copied successfully to network share.")
    except subprocess.CalledProcessError as e:
        print(f"[File Upload To Server]: Error copying files: {e.stderr}")

def delete_file_after_upload(to_remove_file_path):
    print(f"[File Upload To Server]: Removing Local File: {to_remove_file_path}")

    if os.path.exists(to_remove_file_path):
        try:
            if os.path.isdir(to_remove_file_path):
                shutil.rmtree(to_remove_file_path)  # Delete directory (including contents)
            else:
                os.remove(to_remove_file_path)  # Delete file
            print(f"[File Upload To Server]: Successfully removed: {to_remove_file_path}")
        except Exception as e:
            print(f"[File Upload To Server]: Error deleting {to_remove_file_path}: {e}")

def file_upload_to_server(local_file_path, record_user_obj):
    local_file_path = os.path.abspath(local_file_path)  # Ensure absolute path
    remote_folder = record_user_obj['usercode']
    server_address = record_user_obj['server_ip']
    share_name = record_user_obj['server_share_folder_name']
    username = record_user_obj['server_user_name'].replace("\\\\", "\\")
    password = record_user_obj['server_password']

    # Start file upload in a separate thread
    file_upload_thread = threading.Thread(
        target=create_and_copy_to_network_share,
        args=(local_file_path, remote_folder, server_address, share_name, username, password)
    )
    file_upload_thread.start()
    file_upload_thread.join()

def meeting_vote_result_upload_to_server(local_file_path, record_user_obj):
    local_file_path = os.path.abspath(local_file_path)  # Ensure absolute path
    remote_folder = record_user_obj['usercode']
    server_address = record_user_obj['server_ip']
    share_name = record_user_obj['server_share_folder_name']
    username = record_user_obj['server_user_name'].replace("\\\\", "\\")
    password = record_user_obj['server_password']

    # Start file upload in a separate thread
    meeting_vote_file_upload_thread = threading.Thread(
        target=file_upload_meeting_vote_result,
        args=(local_file_path, remote_folder, server_address, share_name, username, password)
    )
    meeting_vote_file_upload_thread.start()

def file_upload_meeting_vote_result(local_folder, remote_folder, server_address, share_name, username, password):
    print(f"[File Upload To Server][Meeting Vote Result]:[Start Uploading...]")

    # Ensure local folder exists
    if not os.path.exists(local_folder):
        print(f"[File Upload To Server]: Local folder does not exist: {local_folder}")
        return

    local_folder = os.path.abspath(local_folder)  # Ensure absolute path

    # Logging (excluding password for security)
    print(f"[File Upload To Server]:[Server Address]: {server_address}")
    print(f"[File Upload To Server]:[Local Folder]: {local_folder}")
    print(f"[File Upload To Server]:[Remote Folder]: {remote_folder}")
    print(f"[File Upload To Server]:[Share Name]: {share_name}")
    print(f"[File Upload To Server]:[User Name]: {username}")

    meeting_vote_folder_name="MeetingVoteResult"   
    # Step 3: Copy files from local folder to the network share
    copy_command = [
        "smbclient", f"//{server_address}/{share_name}", "-U", f"{username}%{password}",
        "--option=client min protocol=SMB2", "--option=client max protocol=SMB3",
        "-c", f'lcd "{local_folder}"; cd "{meeting_vote_folder_name}/{remote_folder}"; prompt OFF; recurse ON; mput *'
    ]
    try:
        subprocess.run(copy_command, check=True, capture_output=True, text=True)
        print(f"[File Upload To Server]: Files copied successfully to network share.")
    except subprocess.CalledProcessError as e:
        print(f"[File Upload To Server]: Command failed: {e.cmd}")
        print(f"[File Upload To Server]: Exit code: {e.returncode}")
        print(f"[File Upload To Server]: Stdout: {e.stdout}")
        print(f"[File Upload To Server]: Stderr: {e.stderr}")

