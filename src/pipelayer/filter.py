from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from functools import wraps
from typing import Any, Callable, List, Optional, Tuple, Union, cast

from pipelayer.context import Context
from pipelayer.enum import Action, State
from pipelayer.event_args import FilterEventArgs
from pipelayer.protocol import FilterEventHandlerT, IFilter


class EventHandlerList(List[FilterEventHandlerT]):
    def append(self, handler: FilterEventHandlerT) -> None:
        super().append(handler)

    def __iadd__(self, handlers: Union[FilterEventHandlerT, Iterable[FilterEventHandlerT]]) -> EventHandlerList:
        return EventHandlerList(super().__iadd__(handlers if isinstance(handlers, Iterable) else [handlers]))

    def __add__(self, handlers: Union[FilterEventHandlerT, Iterable[FilterEventHandlerT]]) -> EventHandlerList:
        return EventHandlerList(super().__add__(
            EventHandlerList(handlers)
            if isinstance(handlers, Iterable)
            else EventHandlerList([handlers])
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

        self.__start: EventHandlerList = EventHandlerList()
        self.__exit: EventHandlerList = EventHandlerList()
        self.__end: EventHandlerList = EventHandlerList()

    # region Properties

    @property
    def name(self) -> str:
        return self.__name

    # region Event Handlers

    @property
    def start(self) -> EventHandlerList:
        return self.__start

    @start.setter
    def start(self, value: EventHandlerList) -> None:
        if not isinstance(value, EventHandlerList):
            raise TypeError("Value must be an instance of EventHandlerList")
        self.__start = value

    @property
    def exit(self) -> EventHandlerList:
        return self.__exit

    @exit.setter
    def exit(self, value: EventHandlerList) -> None:
        if not isinstance(value, EventHandlerList):
            raise TypeError("Value must be an instance of EventHandlerList")
        self.__exit = value

    @property
    def end(self) -> EventHandlerList:
        return self.__end

    @end.setter
    def end(self, value: EventHandlerList) -> None:
        if not isinstance(value, EventHandlerList):
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


def _parse_args(*args: str, **kwargs: dict) -> Tuple[IFilter, Any, Context]:

    if len(args) == 3:
        return cast(IFilter, args[0]), args[1], cast(Context, args[2])

    _self = None
    _data = None
    _context = None
    _args: list = list(args)

    if _args and isinstance(args[0], IFilter):
        _self = cast(IFilter, _args[0])
        _args.pop(0)

    if _args:
        _data = _args[0]
        _args.pop(0)

    if kwargs:
        _data = _data or kwargs.get("data")
        _context = _context or kwargs.get("context")

    return cast(IFilter, _self), _data, cast(Context, _context) if _context else Context()


def raise_events(func: Callable) -> Callable:
    """
    Decorates a filter method to raise events
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        filter, data, context = _parse_args(*args, **kwargs)

        evt_args = FilterEventArgs(data, context, State.RUNNING)

        filter._on_start(evt_args)

        if evt_args.action in (Action.EXIT, Action.SKIP):
            evt_args.state = State.SKIPPING if evt_args.action == Action.SKIP else State.EXITING
            filter._on_exit(evt_args)
            return evt_args.data

        data = func(*args, **kwargs)

        evt_args = FilterEventArgs(data, context, State.COMPLETING)
        filter._on_end(evt_args)

        if evt_args.action is Action.EXIT:
            evt_args.state = State.EXITING
            filter._on_exit(evt_args)
            return evt_args.data

        return data
    return wrapper
