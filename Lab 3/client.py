from http.client import HTTPConnection

connection = HTTPConnection('127.0.0.1', 9090, timeout=10)
connection.request("GET", "/")
response = connection.getresponse()
print(response.read())

connection.close()
