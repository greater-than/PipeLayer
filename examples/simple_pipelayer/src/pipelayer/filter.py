from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, Optional

from pipelayer.context import Context
from pipelayer.step import Step


class Filter(Step):
    def __init__(self: Filter, name: str = "", pre_process: Callable = None, post_process: Callable = None) -> None:
        super().__init__(name)
        self.__pre_process = pre_process
        self.__post_process = post_process

    @property
    def pre_process(self) -> Optional[Callable]:
        return self.__pre_process

    @property
    def post_process(self) -> Optional[Callable]:
        return self.__post_process

    @abstractmethod
    def run(self, data: Any, context: Context) -> Any:
        raise NotImplementedError
