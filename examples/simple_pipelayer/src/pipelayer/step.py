from __future__ import annotations

from abc import ABC
from typing import Any


class Step(ABC):
    def __init__(self: Step, name: str = "") -> None:
        self.__name = name or self.__class__.__name__

    @property
    def name(self) -> str:
        return self.__name

    def run(self, data: Any, context: Any) -> Any:
        raise NotImplementedError
