from enum import Enum

from http_server.http import HTTP_ENCODING, HTTP_LINE_BR


class Method(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    UNSUPPORTED = "UNSUPPORTED"


# possibly add get parameters
class Request:
    def __init__(self, bytes: bytes):
        # set encoding in upper class
        buffer = bytes.decode(HTTP_ENCODING)
        lines = buffer.split(HTTP_LINE_BR)
        start_line = lines.pop(0)
        headers_list = []
        while lines:
            line = lines.pop(0)
            if line == "":
                break
            headers_list.append(line)
        body = HTTP_LINE_BR.join(lines)
        self.parse_start_line(start_line)
        self.parse_headers(headers_list)
        self.body = body

    def parse_start_line(self, start_line: str):
        fields = start_line.split(" ")
        # just reject
        # if len(fields) != 3:
        #     raise NotImplementedError("Unsupported format")
        str_method, self.uri, self.http_version = fields
        try:
            method = Method[str_method]
        except KeyError:
            method = Method.UNSUPPORTED
        self.method = method

    # possibly headers might have multiple values
    # can there be multiple?
    def parse_headers(self, headers_list: list):
        headers = {}
        for header in headers_list:
            header_fileds = header.split(": ")
            key = header_fileds.pop(0).lower()
            value = ": ".join(header_fileds)
            headers[key] = value
        self.__headers = headers

    def get_header(self, key: str) -> str | None:
        return self.__headers.get(key.lower())
