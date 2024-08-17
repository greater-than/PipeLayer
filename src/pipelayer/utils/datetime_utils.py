import datetime as d
import sys


def get_now_utc() -> d.datetime:
    py_major = sys.version_info.major
    py_minor = sys.version_info.minor
    if py_major >= 3 and py_minor < 11:
        return d.utcnow()  # type: ignore
    elif py_major >= 3 and py_minor >= 11:
        return d.datetime.now(d.UTC)  # type: ignore
    else:
        raise Exception("This version of Python is not supported.")
