from enum import Enum


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

class Request:
    def __init__(self, bytes: bytes):
        # set encoding in upper class
        buffer = bytes.decode("ascii")
        lines = buffer.split("\r\n")
        start_line = lines.pop(0)
        headers = []
        while lines:
            line = lines.pop(0)
            if line == "":
                break
            headers.append(line)
        body = "\r\n".join(lines)
        self.parse_start_line(start_line)
        self.headers = headers
        self.body = body

    def parse_start_line(self, start_line: str):
        fields = start_line.split(" ")
        if len(fields) != 3:
            # do sum
            pass
        str_method, self.uri, self.http_version = fields
        try:
            method = Method[str_method]
            self.method = method
        except ValueError:
            # do sum
            pass
