import http.client
from http.client import HTTPConnection
import os

ROOT = "client_directory"


def main():
    host, port = input("Введите адрес сервера: ").strip(), int(input("Введите порт сервера: ").strip())
    connection = HTTPConnection(host, port, timeout=1)
    print("Клиент подключён", "Вы можете использовать команды для взаимодействия с файловым хранилищем",
          "Введите HELP для получения списка доступных команд", sep="\n", end="\n\n\n")
    try:
        while True:
            command = input(">> ").strip().split()
            if command[0] == "HELP":
                print("Синтаксис доступных команд:",
                      "GET {server_file_path}",
                      "Загрузить заданный файл с сервера",
                      "",
                      "POST {server_file_path} {client_file_path|text_string}",
                      "Добавить содержимое файла|строку в конец файла на сервере",
                      "",
                      "PUT {server_file_path|server_directory_path} [file_path|text_string|'-d']",
                      "Перезаписать|создать файл на сервере содержимым файла|пустой или непустой строкой",
                      "Создать пустую директорию",
                      "",
                      "MOVE {server_file_path_from|server_dir_path_from} {server_file_path_to}",
                      "Переместить файл на серевере",
                      "",
                      "COPY {server_file_path_from|server_dir_path_from} {server_dir_path_to}",
                      "Скопировать файл на сервере",
                      "",
                      "DELETE {server_file_path|server_dir_path}",
                      "Удалить файл на сервере",
                      "",
                      "HIERARCHY",
                      "Вывести структуру файловой системы сервера",
                      "",
                      "HELP",
                      "Показать справку о командах клиента",
                      "",
                      "EXIT",
                      "Завершить сессию",
                      sep="\n\t", end="\n\n\n")
                continue
            elif command[0] == "GET":
                connection.request("GET", "/get", body=f"{command[1]}")
                response = connection.getresponse()
                msg, filename, filedata = response.read().split("<$$>".encode())
                with open(f"./client_directory/{filename.decode()}", "wb") as f:
                    f.write(filedata)
                print(msg.decode(), end="\n\n\n")
                continue
            elif command[0] == "POST":
                with open("temp.txt", "wb+") as f:
                    f.write(f"{command[1]}<$$>".encode())
                    try:
                        with open(command[2], "rb") as file:
                            f.write(file.read())
                    except FileNotFoundError:
                        f.write(command[2].encode())
                    except IsADirectoryError:
                        print("Директория не может служить источником данных для записи", end="\n\n\n")
                        continue
                    f.seek(0, os.SEEK_SET)
                    connection.request("POST", "/post", body=f)
                os.system("rm temp.txt")
            elif command[0] == "PUT":
                if len(command) == 2:
                    command.append("")
                with open("temp.txt", "wb+") as f:
                    f.write(f"{command[1]}<$$>".encode())
                    try:
                        with open(command[2], "rb") as file:
                            f.write(file.read())
                    except FileNotFoundError:
                        f.write(command[2].encode())
                    except IsADirectoryError:
                        print("Директория не может служить источником данных для записи", end="\n\n\n")
                        continue
                    f.seek(0, os.SEEK_SET)
                    connection.request("PUT", "/put", body=f)
                os.system("rm temp.txt")
            elif command[0] == "COPY":
                connection.request("COPY", "/copy", body=f"{command[1]} {command[2]}")
            elif command[0] == "MOVE":
                connection.request("MOVE", "/move", body=f"{command[1]} {command[2]}")
            elif command[0] == "DELETE":
                connection.request("DELETE", "/delete", body=command[1])
            elif command[0] == "HIERARCHY":
                connection.request("HIERARCHY", "/hierarchy")
            elif command[0] == "EXIT":
                break
            try:
                response = connection.getresponse()
            except http.client.ResponseNotReady:
                pass
            else:
                print(response.read().decode(), end="\n\n\n")
    except KeyboardInterrupt:
        pass
    connection.close()
    print("Сессия завершена")


if __name__ == "__main__":
    main()
