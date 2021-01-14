from typing import Any

from steampipe.context import Context
from steampipe.step import Step


class MockStep(Step):
    """
    For patching pipeline steps in unit tests
    """

    def run(self, context: Context, data: Any) -> Any:
        return data
