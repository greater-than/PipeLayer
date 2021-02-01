from __future__ import annotations

from enum import Enum
from typing import Any, Protocol, Union, runtime_checkable

from pipelayer.context import Context


class StepType(Enum):
    PIPELINE = "pipeline"
    FILTER = "filter"
    FUNCTION = "function"


@runtime_checkable
class Step(Protocol):
    def run(self, data: Any, context: Union[Context, None]) -> Any:
        raise NotImplementedError
