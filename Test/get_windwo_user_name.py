import subprocess


def get_full_username():
        try:
            full_username = subprocess.check_output("whoami", shell=True, text=True).strip()
            return full_username
        except subprocess.CalledProcessError:
            return None
        
print(f"Current Window User Name: {get_full_username()}")