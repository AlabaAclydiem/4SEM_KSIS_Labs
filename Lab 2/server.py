import socket
import sys
import threading

if len(sys.argv) != 3:
    print("Incorrect parameters.\n Correct pattern: script_path, IP address, port number")
    exit()

clients = []


def client_thread(conn, addr):
    conn.send("Connected to the chat!".encode('utf-8'))
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
        except socket.error as err:
            print(f"Error while receiving data from client: {str(err)}")
            remove(conn)
            break
        else:
            if message != "%end":
                message = f"<{addr}> {message}"
                print(message)
                broadcast(message.encode('utf-8'), conn)
            else:
                print(f"<{addr}> exited")
                conn.send("%end".encode('utf-8'))
                broadcast(f"<{addr}> exited".encode('utf-8'), conn)
                remove(conn)
                break


def broadcast(message, conn):
    for client in clients:
        if client != conn:
            try:
                client.send(message)
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
            host, port = str(sys.argv[1]), int(sys.argv[2])
            if not server.bind((host, port)):
                print("Port is open, connected")
                server.listen(100)
                while True:
                    connection, address = server.accept()
                    clients.append(connection)
                    print(f"{address} connected")
                    threading.Thread(target=client_thread, args=(connection, address,), daemon=True).start()
            else:
                print("Port is not open")
    except socket.error as err:
        print(f"Error while creating socket: {str(err)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted manually")
