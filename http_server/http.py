HTTP_VER = "HTTP/1.1"
HTTP_SERVER_NAME = "insomma"
HTTP_LINE_BR = "\r\n"
HTTP_ENCODING = "ascii"

STATUS_CODES = {
    # 2xx
    200: "200 OK",
    201: "201 Created",
    202: "202 Accepted",
    203: "203 Non-Authoritative Information",
    204: "204 No Content",
    205: "205 Reset Content",
    206: "206 Partial Content",
    207: "207 Multi-Status",
    208: "208 Already Reported",
    226: "226 IM Used",
    # 4xx
    404: "404 Not Found",
    # 5xx
    500: "500 Internal Server Error",
    501: "501 Not Implemented",
}
