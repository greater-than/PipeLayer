from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (Any, Callable, Iterable, List, Optional, Tuple, TypeVar,
                    Union)

from pipelayer._patch.typing import Protocol, runtime_checkable  # type: ignore
from pipelayer.context import Context
from pipelayer.event_args import FilterEventArgs


@runtime_checkable
class IManifest(Protocol):  # pragma: no cover
    name: str
    step_type: Enum
    steps: List
    start: datetime
    end: Optional[datetime]
    duration: Optional[datetime]


@runtime_checkable
class IStep(Protocol):  # pragma: no cover
    def run(self, data: Any, context: Optional[Context]) -> Any:
        pass


@runtime_checkable
class IFilter(Protocol):  # pragma: no cover
    @property
    def name(self) -> str:
        pass

    @property
    def start(self) -> IEventHandlerList:
        pass

    @start.setter
    def start(self, value: IEventHandlerList) -> None:
        pass

    @property
    def exit(self) -> IEventHandlerList:
        pass

    @exit.setter
    def exit(self, value: IEventHandlerList) -> None:
        pass

    @property
    def end(self) -> IEventHandlerList:
        pass

    @end.setter
    def end(self, value: IEventHandlerList) -> None:
        pass

    def run(self, data: Any, context: Any) -> Any:
        pass

    def _on_start(self, args: FilterEventArgs) -> None:
        pass

    def _on_exit(self, args: FilterEventArgs) -> None:
        pass

    def _on_end(self, args: FilterEventArgs) -> None:
        pass


@runtime_checkable
class ICompoundStep(Protocol):  # pragma: no cover

    @property
    def name(self) -> str:
        pass

    @property
    def manifest(self) -> IManifest:
        pass

    def run(self, data: Any, context: Any) -> Any:
        pass

    def _run(self, data: Any, context: Any) -> Tuple[Any, IManifest]:
        pass


PipelineCallableT = TypeVar("PipelineCallableT", bound=Callable[[Any, Context], Any])
FilterEventHandlerT = TypeVar("FilterEventHandlerT", bound=Callable[[IFilter, FilterEventArgs], None])


class IEventHandlerList(Iterable[FilterEventHandlerT]):  # pragma: no cover

    def append(self, handler: FilterEventHandlerT) -> None:
        pass

    def __iadd__(self, handlers: Union[FilterEventHandlerT, Iterable[FilterEventHandlerT]]) -> IEventHandlerList:
        pass

    def __add__(self, handlers: Union[FilterEventHandlerT, Iterable[FilterEventHandlerT]]) -> IEventHandlerList:
        pass
