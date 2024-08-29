import socket

def check_server(address, port):
    s = socket.socket()
    try:
        s.connect((address, port))
        print(f"Connection to {address}:{port} successful")
    except ConnectionRefusedError:
        print(f"Connection to {address}:{port} refused")
    except Exception as e:
        print(f"Error connecting to {address}:{port}: {e}")
    finally:
        s.close()

check_server('192.168.43.157',5090)