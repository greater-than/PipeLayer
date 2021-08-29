from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, List, Optional, Union

from pipelayer.event_args import FilterEventArgs
from pipelayer.protocol import FilterEventHandlerT


class FilterEventHandlerList(List[FilterEventHandlerT]):
    def append(self, handler: FilterEventHandlerT) -> None:
        super().append(handler)

    def __iadd__(self, handlers: Union[FilterEventHandlerT, Iterable[FilterEventHandlerT]]) -> FilterEventHandlerList:
        return FilterEventHandlerList(super().__iadd__(handlers if isinstance(handlers, Iterable) else [handlers]))

    def __add__(self, handlers: Union[FilterEventHandlerT, Iterable[FilterEventHandlerT]]) -> FilterEventHandlerList:
        return FilterEventHandlerList(super().__add__(
            FilterEventHandlerList(handlers)
            if isinstance(handlers, Iterable)
            else FilterEventHandlerList([handlers])
        ))


class Filter(ABC):
    """
    The Filter abstract class.
    """

    def __init__(
        self: Filter,
        name: Optional[str] = "",
    ) -> None:
        self.__name = name or self.__class__.__name__

        self.__start: FilterEventHandlerList = FilterEventHandlerList()
        self.__exit: FilterEventHandlerList = FilterEventHandlerList()
        self.__end: FilterEventHandlerList = FilterEventHandlerList()

    # region Properties

    @property
    def name(self) -> str:
        return self.__name

    # region Event Handlers

    @property
    def start(self) -> FilterEventHandlerList:
        return self.__start

    @start.setter
    def start(self, value: FilterEventHandlerList) -> None:
        if not isinstance(value, FilterEventHandlerList):
            raise TypeError("Value must be an instance of EventHandlerList")
        self.__start = value

    @property
    def exit(self) -> FilterEventHandlerList:
        return self.__exit

    @exit.setter
    def exit(self, value: FilterEventHandlerList) -> None:
        if not isinstance(value, FilterEventHandlerList):
            raise TypeError("Value must be an instance of EventHandlerList")
        self.__exit = value

    @property
    def end(self) -> FilterEventHandlerList:
        return self.__end

    @end.setter
    def end(self, value: FilterEventHandlerList) -> None:
        if not isinstance(value, FilterEventHandlerList):
            raise TypeError("Value must be an instance of EventHandlerList")
        self.__end = value

    # endregion

    # endregion
    # region Runner

    @abstractmethod
    def run(self: Filter, data: Any, context: Any) -> Any:
        raise NotImplementedError

    # endregion
    # region Events

    def _on_start(self, args: FilterEventArgs) -> None:
        [e(self, args) for e in self.start]

    def _on_exit(self, args: FilterEventArgs) -> None:
        [e(self, args) for e in self.exit]

    def _on_end(self, args: FilterEventArgs) -> None:
        [e(self, args) for e in self.end]

    # endregion
