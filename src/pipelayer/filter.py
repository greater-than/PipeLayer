from __future__ import annotations

from abc import ABC, abstractmethod
from functools import wraps
from typing import Any, Callable, List, Optional

from pipelayer.context import Context
from pipelayer.enum import Action, State
from pipelayer.event_args import FilterEventArgs


def raise_events(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        filter: Filter = args[0]
        data: Any = args[1]
        context: Context = args[2]

        evt_args = FilterEventArgs(data, context, State.RUNNING)

        filter._on_start(evt_args)

        if evt_args.action in (Action.EXIT, Action.SKIP):
            evt_args.state = State.SKIPPING if evt_args.action == Action.SKIP else State.EXITING
            filter._on_exit(evt_args)
            return evt_args.data

        data = func(*args, **kwargs)

        evt_args = FilterEventArgs(data, args[2], State.COMPLETING)
        filter._on_end(evt_args)

        if evt_args.action is Action.EXIT:
            evt_args.state = State.EXITING
            filter._on_exit(evt_args)
            return evt_args.data

        return data
    return wrapper


class Filter(ABC):
    """
    The Filter abstract class.
    """

    def __init__(
        self: Filter,
        name: Optional[str] = "",
        pre_process: Optional[Callable[[Any, Context], Any]] = None,
        post_process: Optional[Callable[[Any, Context], Any]] = None
    ) -> None:
        self.__name = name or self.__class__.__name__
        self.__pre_process = pre_process
        self.__post_process = post_process

        self.__start: List[Callable] = []
        self.__exit: List[Callable] = []
        self.__end: List[Callable] = []

    # region Properties

    @property
    def name(self) -> str:
        return self.__name

    @property
    def pre_process(self) -> Optional[Callable]:
        return self.__pre_process

    @property
    def post_process(self) -> Optional[Callable]:
        return self.__post_process

    # region Events

    @property
    def start(self) -> List[Callable[[Filter, FilterEventArgs], Any]]:
        if not self.__start:
            self.__start = []
        return self.__start

    @property
    def exit(self) -> List[Callable[[Filter, FilterEventArgs], Any]]:
        if not self.__exit:
            self.__exit = []
        return self.__exit

    @property
    def end(self) -> List[Callable[[Filter, FilterEventArgs], Any]]:
        if not self.__end:
            self.__end = []
        return self.__end

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
