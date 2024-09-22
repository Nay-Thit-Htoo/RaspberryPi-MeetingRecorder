import os

class FileService:
    def __init__(self, folder_name, destination_path):
        self.folder_name = folder_name
        self.destination_path = destination_path

    def create_folder(self):
        # Combine destination path with the folder name
        full_path = os.path.join(self.destination_path, self.folder_name)
        
        try:
            # Create the folder
            os.makedirs(full_path, exist_ok=True)
            print(f"Folder '{self.folder_name}' created at: {full_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
