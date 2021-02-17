from typing import Callable


def authorize_decorator(func) -> Callable:
    def wrapper(*args, **kwargs):
        from flask import request
        hdrs = request.headers
        # Could add header token validation or retrieve correlation id, etc.
        # auth_token = hdrs.get("token")
        # correlation_id = hdrs.get("correlationId")
        return func(*args, **kwargs, http_header=hdrs)
    return wrapper
