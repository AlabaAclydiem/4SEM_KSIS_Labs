import struct


def message_out(connection, name):
    while True:
        msg = input()
        message = f"{name}: {msg}".encode("utf-8")
        message = struct.pack(">I", len(message)) + message
        if connection:
            connection.send(message)
        else:
            return True
        if msg.split(" ", 1)[-1] == "q":
            return True


def message_in(connection):
    size, data = struct.unpack(">I", connection.recv(4))[0], bytes()
    while len(data) < size:
        data += connection.recv(size - len(data))
    data = data.decode("utf-8")
    print(data)
