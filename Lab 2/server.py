import socket

from msgprocess import message_in, message_out

HOST = "127.0.0.1"
PORT = 9090

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    connection, address = server.accept()
    print(f"Connected by {address}")
    # inthread = threading.Thread(target=message_in, args=(connection,), daemon=True)
    # inthread.start()
    while True:
        message_in(connection)
        if message_out(connection, "Server"):
            break

print("Session ended")
