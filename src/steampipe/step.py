from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Union

from steampipe.context import Context


class Step(ABC):
    def __init__(self: Step, name: str = "", pre_process: Callable = None, post_process: Callable = None):
        self.__name = name or self.__class__.__name__
        self.__pre_process = pre_process
        self.__post_process = post_process

    @property
    def name(self) -> str:
        return self.__name

    @property
    def pre_process(self) -> Union[Callable, None]:
        return self.__pre_process

    @property
    def post_process(self) -> Union[Callable, None]:
        return self.__post_process

    @abstractmethod
    def execute(self, context: Context, data: Any = None) -> Any:
        raise NotImplementedError