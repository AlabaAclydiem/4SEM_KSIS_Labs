import socket
import sys
import select

if len(sys.argv) != 3:
    print("Incorrect parameters.\n Correct pattern: script_path, IP address, port number")
    exit()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        host, port = str(sys.argv[1]), int(sys.argv[2])
        input_list = [sys.stdin, client]
        if not client.connect_ex((host, port)):
            try:
                while True:
                    read_input, _, _ = select.select(input_list, [], [])
                    for ipt in read_input:
                        if ipt == client:
                            message = client.recv(1024).decode('utf-8')
                            if message != "%end":
                                print(message)
                            else:
                                raise StopIteration
                        else:
                            sys.stdout.flush()
                            message = input()
                            try:
                                client.send(message.encode('utf-8'))
                            except socket.error as err:
                                print(f"Error while sending data to client: {str(err)}")
                                raise StopIteration
            except StopIteration:
                pass
        else:
            print("There's no server here")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted manually")
