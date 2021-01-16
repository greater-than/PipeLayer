from typing import Any

from pipelayer.context import Context
from pipelayer.filter import Filter


class MockFilter(Filter):
    """
    For patching pipeline filters in unit tests
    """

    def run(self, context: Context, data: Any) -> Any:
        return data
