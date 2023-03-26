import struct


def message_out(connection, name):
    while True:
        if connection:
            msg = input()
            if msg != "q":
                message = f"{name}: {msg}".encode("utf-8")
                message = struct.pack(">I", len(message)) + message
                connection.send(message)
            else:
                message = f"{name} disconnected".encode("utf-8")
                message = struct.pack(">I", len(message)) + message
                connection.send(message)
                break
        else:
            break


def message_in(connection):
    while True:
        size, data = struct.unpack(">I", connection.recv(4))[0], bytes()
        while len(data) < size:
            data += connection.recv(size - len(data))
        data = data.decode("utf-8")
        print(data)
        if data.endswith("disconnected"):
            break
