HTTP_VER = "HTTP/1.1"
HTTP_LINE_BR = "\r\n"

# decorator take tuple as status code and body and creates respose accordingly
STATUS_CODES = {
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
}

def http_response(status_code, body=None) -> bytes:
    response = [
        f"{HTTP_VER} {STATUS_CODES[status_code]}",
        "Server: INSOMMA",
        "Connection: close"
    ]
    if body is not None:
        response.extend([
            f"Content-Length: {len(body)}",
            "",
            body
        ])
    return HTTP_LINE_BR.join(response).encode("ascii")
