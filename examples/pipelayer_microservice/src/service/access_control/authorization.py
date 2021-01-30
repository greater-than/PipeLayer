from typing import Callable


def authorize_decorator(func) -> Callable:
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
