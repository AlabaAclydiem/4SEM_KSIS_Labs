import socket

from msgprocess import message_in, message_out

HOST = "127.0.0.1"
PORT = 9090

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    client.connect((HOST, PORT))
    while True:
        if message_out(client, "Client"):
            break
        message_in(client)
