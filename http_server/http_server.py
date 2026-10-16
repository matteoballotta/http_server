import inspect
import socket
from collections.abc import Callable
from functools import wraps
from typing import Any

from http_server.http import (
    HTTP_ENCODING,
    HTTP_LINE_BR,
    HTTP_VER,
    STATUS_CODES,
)
from http_server.log import log
from http_server.request import Request

routes = {}


class HTTPServer:
    def __init__(self, host="localhost", port=8080, listen=5, timeout=30):
        self.routes = {}
        self.host = host
        self.port = port
        self.timeout = timeout
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((host, port))
        self.serversocket.listen(listen)
        log(f"Server started at http://{host}:{port}")

    def run(self):
        while True:
            connection, address = self.serversocket.accept()
            connection.settimeout(self.timeout)
            client_ip, client_port = address
            client_address = f"{client_ip}:{client_port}"
            log(f"({client_address}) Connected")
            status_code, body = 500, None
            request = None
            while True:
                try:
                    buf = connection.recv(4096)
                except TimeoutError:
                    break
                if not buf:
                    break
                request = Request(buf)
                log(f"({client_address}) {request.method.value} -> {request.uri} {len(request.body)}")
                try:
                    handler = self.routes[request.uri.split("?")[0]]
                    status_code, body = handler(request, connection, address)
                except KeyError:
                    status_code, body = 404, "Not Found"
                except NotImplementedError:
                    status_code = 501
                log(
                    f"({client_address}) {request.uri if request else "..."} <- {status_code} {0 if body is None else len(body)}"
                )
                headers = []
                if request.get_header("Connection") == "close":
                    headers.append("Connection: close")
                else:
                    # MAX REQUESTS implement
                    headers.append("Connection: keep-alive, max=0")
                # if status code is not implemented do something
                response = HTTPServer.http_response(status_code, headers, body)
                connection.sendall(response)

            connection.close()
            log(f"({client_address}) Disconnected")
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
    def http_response(status_code, headers: list[str] | None = None, body=None) -> bytes:
        response = [f"{HTTP_VER} {STATUS_CODES[status_code]}"]
        if headers is not None:
            response.extend(headers)
        if body is not None:
            response.extend([f"Content-Length: {len(body)}", "", body])
        return HTTP_LINE_BR.join(response).encode(HTTP_ENCODING)
