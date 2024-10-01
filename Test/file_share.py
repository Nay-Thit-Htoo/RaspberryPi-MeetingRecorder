import os

def check_world_writable(network_path):       
        test_file = os.path.join(network_path, "test_write.txt")
        try:
            # Try writing a test file
            with open(test_file, "w") as file:
                file.write("This is a test to check if the folder is writable.")
            print(f"Success: The folder {network_path} is writable.")
            
            # Optionally, clean up by removing the test file
            os.remove(test_file)
        except Exception as e:
            print(f"Error: Cannot write to the folder {network_path}. Error: {e}")
check_world_writable(r"\\NAYTHITHTOO\Recording")