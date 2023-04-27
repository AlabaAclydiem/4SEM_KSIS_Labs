from http.server import HTTPServer, BaseHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 9090
ROOT = "server_directory"


class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        with open(f"{ROOT}/test.txt", "rb") as file:
            self.wfile.write(file.read())


server = HTTPServer((HOST, PORT), CustomHTTPRequestHandler)
server.serve_forever()
server.server_close()
