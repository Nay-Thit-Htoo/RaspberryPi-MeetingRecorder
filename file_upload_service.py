import os
import shutil
import threading

def upload_file_thread(local_file_path,record_user_obj):
    print(f"[File Upload To Server]:[Start Uploading...]")
    file_name = os.path.basename(local_file_path)
    server_file_path=rf"{record_user_obj['upload_file_path']}"    
    create_dest_folder_path = os.path.join(server_file_path,record_user_obj['usercode'])   
    os.makedirs(create_dest_folder_path, exist_ok=True)  

    to_upload_dest_path=os.path.join(create_dest_folder_path,file_name)
    try:
        # Copy the file to the network share
        shutil.copy2(local_file_path, to_upload_dest_path)
        print(f"[File Upload To Server]: [Successfully Uploaded...] {file_name}")        
    except Exception as e:
        print(f"[File Upload To Server]:[Failed to upload file: {str(e)}]") 

def delete_file_after_upload(to_remove_file_path):
     print(f"[File Upload To Server]:[Remove Local File After Upload] {to_remove_file_path}")
     if os.path.exists(to_remove_file_path):
        os.remove(to_remove_file_path)
        print(f"[File Upload To Server]:[Successfully Remove Local File] {to_remove_file_path}") 

def file_upload_to_server(local_file_path,record_user_obj):
    file_upload_thread = threading.Thread(target=upload_file_thread, args=(local_file_path,record_user_obj))
    file_upload_thread.start()
    file_upload_thread.join()