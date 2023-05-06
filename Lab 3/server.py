from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import shutil

ROOT = "server_directory"


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def basic_headers(self):
        self.send_response(200)
        self.end_headers()

    def read_data(self):
        if "Content-Length" in self.headers:
            content_length = int(self.headers["Content-Length"])
            body = self.rfile.read(content_length)
            return body
        elif "chunked" in self.headers.get("Transfer-Encoding", ""):
            body = bytearray()
            while True:
                line = self.rfile.readline().strip()
                chunk_length = int(line, 16)
                if chunk_length != 0:
                    chunk = self.rfile.read(chunk_length)
                    body += chunk
                self.rfile.readline()
                if chunk_length == 0:
                    break
            return body
        return bytes()

    def do_GET(self):
        self.basic_headers()
        file = f"./{ROOT}/{self.read_data().decode()}"
        try:
            with open(file, "rb") as f:
                self.wfile.write("Файл успешно получен<$$>".encode())
                self.wfile.write(f"{file.split('/')[-1]}<$$>".encode())
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.wfile.write("Запрашиваемого файла не существует".encode())
        except IsADirectoryError:
            self.wfile.write("Нельзя запросить директорию".encode())

    def do_POST(self):
        self.basic_headers()
        file, data = self.read_data().decode().split("<$$>")
        try:
            with open(f"./{ROOT}/{data}", "rb") as f:
                temp = f.read().decode()
            data = temp
        except (FileNotFoundError, IsADirectoryError):
            pass
        file = f"./{ROOT}/{file}"
        try:
            with open(file, "rb"):
                pass
        except FileNotFoundError:
            self.wfile.write("Файла для записи не существует".encode())
        except IsADirectoryError:
            self.wfile.write("Нельзя записать в директорию".encode())
        else:
            with open(file, "ab") as f:
                f.write(data.encode())
            self.wfile.write("Данные успешно записаны".encode())

    def do_PUT(self):
        self.basic_headers()
        file, data = self.read_data().decode().split("<$$>")
        try:
            with open(f"./{ROOT}/{data}", "rb") as f:
                temp = f.read().decode()
            data = temp
        except (FileNotFoundError, IsADirectoryError):
            pass
        file = f"./{ROOT}/{file}"
        try:
            with open(file, "rb"):
                pass
        except FileNotFoundError:
            if data != "-d":
                with open(file, "wb") as f:
                    f.write(data.encode())
                self.wfile.write("Файл создан, данные успешно записаны".encode())
            else:
                os.mkdir(file)
                self.wfile.write("Директория создана".encode())
        except IsADirectoryError:
            if data != "-d":
                self.wfile.write("Нельзя перезаписать директорию".encode())
            else:
                self.wfile.write("Директория с данным путём уже есть".encode())
        else:
            with open(file, "wb") as f:
                f.write(data.encode())
            self.wfile.write("Данные успешно перезаписаны".encode())

    def do_COPY(self):
        self.basic_headers()
        files = self.read_data().decode().split()
        files = tuple(map(lambda x: f"./{ROOT}/{x}" if x != "." else f"./{ROOT}", files))
        try:
            with open(files[1], "rb"):
                pass
        except FileNotFoundError:
            self.wfile.write("Целевой директории не существует".encode())
        except IsADirectoryError:
            try:
                with open(files[0], "rb"):
                    pass
            except FileNotFoundError:
                self.wfile.write("Копируемые файл или директрия не существуют".encode())
            except IsADirectoryError:
                os.system(f"cp -r {files[0]} {files[1]}")
                self.wfile.write("Директория успешно скопирована".encode())
            else:
                shutil.copy2(files[0], files[1])
                self.wfile.write("Файл успешно скопирован".encode())
        else:
            self.wfile.write("Копирование в файл невозможно".encode())

    def do_MOVE(self):
        self.basic_headers()
        files = self.read_data().decode().split()
        files = tuple(map(lambda x: f"./{ROOT}/{x}" if x != "." else f"./{ROOT}", files))
        try:
            with open(files[1], "rb"):
                pass
        except FileNotFoundError:
            self.wfile.write("Целевой директории не существует".encode())
        except IsADirectoryError:
            try:
                with open(files[0], "rb"):
                    pass
            except FileNotFoundError:
                self.wfile.write("Перемещаемые файл или директрия не существуют".encode())
            except IsADirectoryError:
                shutil.move(files[0], files[1])
                self.wfile.write("Директория успешно перемещена".encode())
            else:
                shutil.move(files[0], files[1])
                self.wfile.write("Файл успешно перемещён".encode())
        else:
            self.wfile.write("Перемещение в файл невозможно".encode())

    def do_DELETE(self):
        self.basic_headers()
        file = f"./{ROOT}/{self.read_data().decode()}"
        try:
            with open(file, "rb"):
                pass
        except FileNotFoundError:
            self.wfile.write("Удаляемые файл или директория не существуют".encode())
        except IsADirectoryError:
            shutil.rmtree(file)
            self.wfile.write("Директория успешно удалена".encode())
        else:
            os.system(f"rm {file}")
            self.wfile.write("Файл успешно удалён".encode())

    def do_HIERARCHY(self):
        self.basic_headers()
        os.system(f"tree {ROOT} >> ./text.txt")
        with open("text.txt", "rb") as f:
            self.wfile.write(f.read())
        os.system(f"rm ./text.txt")


def main():
    host, port = input("Введите адрес сервера: ").strip(), int(input("Введите порт сервера: ").strip())
    server = HTTPServer((host, port), CustomHTTPRequestHandler)
    print("Сервер запущен")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Сервер выключен")


if __name__ == "__main__":
    main()
