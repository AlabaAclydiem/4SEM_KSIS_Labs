import socket
import struct
import threading

clients = []
addr = []


def client_thread(conn, addr):
    message = "Connected to the chat!".encode('utf-16')
    conn.send(struct.pack("<I", len(message)) + message)
    while True:
        try:
            message, size = bytes(), struct.unpack("<I", conn.recv(4))[0]
            while len(message) < size:
                message += conn.recv(size - len(message))
            message = message.decode('utf-16')
        except socket.error as err:
            print(f"Error while receiving data from client: {str(err)}")
            remove(conn)
            break
        else:
            if message != "@exit":
                message = f"<{addr}> {message}"
                print(message)
                broadcast(message.encode('utf-16'), conn)
            else:
                print(f"<{addr}> exited")
                conn.send("@exit".encode('utf-16'))
                broadcast(f"<{addr}> exited".encode('utf-16'), conn)
                remove(conn)
                break


def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(struct.pack("<I", len(message)) + message)
            except socket.error as err:
                print(f"Error while sending data to client: {str(err)}")
                client.close()
                remove(client)


def remove(conn):
    if conn in clients:
        clients.remove(conn)


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            host, port = str(input("Enter server's IP address: ")), int(input("Enter server's port: "))
            if not server.bind((host, port)):
                print("Port is open, connected")
                server.listen(100)
                try:
                    while True:
                        try:
                            connection, address = server.accept()
                        except socket.timeout:
                            pass
                        except KeyboardInterrupt:
                            clients_temp = list(clients)
                            for conn, address in zip(clients_temp, addr):
                                print(f"<{address}> exited")
                                conn.send(struct.pack("<I", len("@exit".encode('utf-16'))) + "@exit".encode('utf-16'))
                                broadcast(f"<{address}> exited".encode('utf-16'), conn)
                            for conn, address in zip(clients_temp, addr):
                                remove(conn)
                                addr.remove(address)
                            break
                        else:
                            clients.append(connection)
                            addr.append(address)
                            print(f"{address} connected")
                            threading.Thread(target=client_thread, args=(connection, address,), daemon=True).start()
                except StopIteration:
                    pass
            else:
                print("Port is not open")
    except socket.error as err:
        print(f"Error while creating socket: {str(err)}")


if __name__ == "__main__":
    main()
