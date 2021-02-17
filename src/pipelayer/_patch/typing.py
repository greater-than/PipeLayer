import sys

if sys.version_info >= (3, 8):  # pragma no cover
    from typing import Protocol, runtime_checkable
else:  # pragma no cover
    from typing_extensions import Protocol, runtime_checkable  # NOQA F401
