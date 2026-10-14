import inspect
import socket
from collections.abc import Callable
from functools import wraps
from typing import Any

from http_server.http import HTTP_LINE_BR, HTTP_SERVER_NAME, HTTP_VER, STATUS_CODES
from http_server.log import log
from http_server.request import Request

routes = {}

class HTTPServer:
    def __init__(self, host="localhost", port=8080, listen=5):
        self.routes = {}
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((host, port))
        self.serversocket.listen(listen)
        log(f"Server started at http://{host}:{port}")


    def run(self):
        while True:
            connection, address = self.serversocket.accept()
            client_ip, client_port = address
            client_address = f"{client_ip}:{client_port}"
            buf = connection.recv(1024)
            status_code, body = 500, None
            try:
                request = Request(buf)
                log(f"({client_address}) {request.method.value} -> {request.uri}")
                handler = self.routes[request.uri.split("?")[0]]
                status_code, body = handler(request, connection, address)
            except KeyError:
                status_code, body = 404, "Not found"
            except NotImplementedError:
                status_code = 501
            finally:
                log(f"({client_address}) ... <- {status_code} {0 if body is None else len(body)}")
                # if status code is not implemented do something
                response = HTTPServer.http_response(status_code, body)
                connection.sendall(response)
                connection.close()
        # find a way to gracefully close
        self.serversocket.close()


    def route(self, path: str):
        def decorator(func: Callable[..., tuple[int, str]]):
            params = inspect.signature(func).parameters
            @wraps(func)
            def inner(
                req: Request,
                conn: socket.socket,
                addr: Any,
            ) -> tuple[int, str]:
                kwargs = {}
                if "req" in params:
                    kwargs["req"] = req
                if "conn" in params:
                    kwargs["conn"] = conn
                if "addr" in params:
                    kwargs["addr"] = addr
                status_code, body = func(**kwargs)
                return status_code, body
            self.routes[path] = inner
            return inner
        return decorator


    @staticmethod
    def http_response(status_code, body=None) -> bytes:
        response = [
            f"{HTTP_VER} {STATUS_CODES[status_code]}",
            f"Server: {HTTP_SERVER_NAME}",
            "Connection: close",
        ]
        if body is not None:
            response.extend([f"Content-Length: {len(body)}", "", body])
        return HTTP_LINE_BR.join(response).encode("ascii")
