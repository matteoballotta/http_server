import inspect


def route(func):
    sig = inspect.signature(func)
    params = sig.parameters
    def inner(req, conn):
        kwargs = {}
        if "req" in params:
            kwargs["req"] = req
        if "conn" in params:
            kwargs["conn"] = conn
        ret = func(**kwargs)
        status_code, body = ret
        conn.sendall(http.http_response(status_code, body))
        conn.close()
        return ret
    return inner
