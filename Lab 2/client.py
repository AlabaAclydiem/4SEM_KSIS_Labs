import socket
import threading

from msgprocess import message_in, message_out

HOST = "192.168.41.136"
PORT = 9090

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    print(f"Connected to {(HOST, PORT)}")
    in_thread = threading.Thread(target=message_in, args=(client,), daemon=True)
    out_thread = threading.Thread(target=message_out, args=(client, "Client",), daemon=True)
    in_thread.start()
    out_thread.start()
    while out_thread.is_alive() and in_thread.is_alive():
        pass

print("Session ended")
