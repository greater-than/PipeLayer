from __future__ import annotations

from abc import abstractmethod
from typing import Any, Callable, Optional

from pipelayer.context import Context


class Filter:
    def __init__(
        self: Filter,
        name: str = "",
        pre_process: Optional[Callable[[Any, Context], Any]] = None,
        post_process: Optional[Callable[[Any, Context], Any]] = None
    ) -> None:
        self.__name = name or self.__class__.__name__
        self.__pre_process = pre_process
        self.__post_process = post_process

    @property
    def name(self) -> str:
        return self.__name

    @property
    def pre_process(self) -> Optional[Callable]:
        return self.__pre_process

    @property
    def post_process(self) -> Optional[Callable]:
        return self.__post_process

    @abstractmethod
    def run(self, data: Any, context: Any) -> Any:
        raise NotImplementedError
