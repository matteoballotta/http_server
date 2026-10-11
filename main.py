# use -v for cURL to see malformed requests
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# booo
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('localhost', 8090))
serversocket.listen(5)

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(1024).decode("ascii")
    lines = buf.split("\r\n")
    start_line = lines.pop(0)
    headers = []
    while lines:
        line = lines.pop(0)
        if line == "":
            break
        headers.append(line)
    body = "\r\n".join(lines)
    print(start_line)
    print(headers)
    print(body)
    connection.send(b"HTTP/1.1 403 Forbidden\r\nServer: Apache\r\n\r\ntest")
    connection.close()

serversocket.close()
