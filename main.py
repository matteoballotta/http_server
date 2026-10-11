# use -v for cURL to see malformed requests
import socket

from decorators import route
from request import Request


@route
def test():
    return 206, "ciao"

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# booo
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(('localhost', 8090))
serversocket.listen(5)

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(1024)
    request = Request(buf)
    # fix decorator parameters
    test(request, connection)


serversocket.close()
