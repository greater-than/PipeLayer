from __future__ import annotations

from abc import ABC
from typing import Any, Union

from pipelayer.context import Context


class Step(ABC):
    def __init__(self: Step, name: str = "") -> None:
        self.__name = name or self.__class__.__name__

    @property
    def name(self) -> str:
        return self.__name

    def run(self, context: Union[Context, Any], data: Any) -> Any:
        raise NotImplementedError
