from enum import EnumMeta
from typing import Any


class EnumContains(EnumMeta):
    def __contains__(cls, item: Any) -> bool:
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True
