import socket

def check_server_connection(address, port):  
    s = socket.socket()
    try:
        s.connect((address, port))
        print(f"Connection to {address}:{port} successful")
        return True
    except ConnectionRefusedError:
        print(f"Connection to {address}:{port} refused")
        return False
    except Exception as e:
        print(f"Error connecting to {address}:{port}: {e}")
        return False
    finally:
        s.close()
