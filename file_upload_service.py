import os
import threading

def upload_file_thread(local_file_path,record_user_obj):
    print(f"[File Upload To Server]:[Start Uploading...]")
    file_name = os.path.basename(local_file_path)
    server_file_path=record_user_obj['upload_file_path']    
    dest_path = os.path.join(server_file_path, file_name)
    
    #file_size = os.path.getsize(local_file_path)  
    with open(local_file_path, 'rb') as src_file:
        with open(dest_path, 'wb') as dest_file:
            while True:
                # Read the file in chunks (64KB)
                chunk = src_file.read(1024)
                if not chunk:
                    break
                dest_file.write(chunk)                 
    print(f"[File Upload To Server]:[Uploaded Successfully...]")
   
def file_upload_to_server(local_file_path,record_user_obj):
    file_upload_thread = threading.Thread(target=upload_file_thread, args=(local_file_path,record_user_obj))
    file_upload_thread.start()
    file_upload_thread.join()