import socket
import sys
import select
import struct


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            input_list = [sys.stdin, client]
            host, port = str(input("Enter server's IP address: ")), int(input("Enter server's port: "))
            if not client.connect_ex((host, port)):
                try:
                    while True:
                        read_input, _, _ = select.select(input_list, [], [])
                        for ipt in read_input:
                            if ipt == client:
                                try:
                                    message, size = bytes(), struct.unpack("<I", client.recv(4))[0]
                                    while len(message) < size:
                                        message += client.recv(size - len(message))
                                    message = message.decode('utf-16')
                                except socket.error as err:
                                    print(f"Error while receiving data from server: {str(err)}")
                                    raise StopIteration
                                else:
                                    if message != "@exit":
                                        print(message)
                                    else:
                                        raise StopIteration
                            else:
                                message = input()
                                try:
                                    client.send(struct.pack("<I", len(message.encode("utf-16"))) +
                                                message.encode('utf-16'))
                                except socket.error as err:
                                    print(f"Error while sending data to server: {str(err)}")
                                    raise StopIteration
                                else:
                                    if message == "@exit":
                                        raise StopIteration
                except (StopIteration, KeyboardInterrupt):
                    client.send(struct.pack("<I", len("@exit".encode("utf-16"))) + "@exit".encode('utf-16'))
            else:
                print("There's no server here")
    except socket.error as err:
        print(f"Error while creating socket: {str(err)}")


if __name__ == "__main__":
    main()
