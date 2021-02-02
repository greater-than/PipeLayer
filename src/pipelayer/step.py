from __future__ import annotations

from enum import Enum
from typing import Any, Protocol, Union, runtime_checkable

from pipelayer.context import Context
from pipelayer.enum_meta import EnumContains


class StepType(Enum, metaclass=EnumContains):
    PIPELINE = "Pipeline"
    SWITCH = "Switch"
    FILTER = "Filter"
    FUNCTION = "Function"


@runtime_checkable
class Step(Protocol):
    def run(self, data: Any, context: Union[Context, None]) -> Any:
        raise NotImplementedError
