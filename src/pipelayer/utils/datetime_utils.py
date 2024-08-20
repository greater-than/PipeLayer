import datetime as d
import sys


def get_now_utc() -> d.datetime:
    if sys.version_info >= (3, 11):
        return d.datetime.now(d.UTC)  # type: ignore
    else:  # pragma: no cover
        return d.datetime.utcnow()
