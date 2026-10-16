# use -v for cURL to see malformed requests
from http_server.http_server import HTTPServer
from http_server.request import Request

server = HTTPServer(host="localhost", port=8090)


@server.route("/test")
def test(req: Request):
    return 206, f"hello {req.get_header("User-Agent")}"


server.run()
