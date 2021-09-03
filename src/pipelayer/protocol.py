from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (Any, Callable, Iterable, List, Optional, Tuple, TypeVar,
                    Union)

from pipelayer._patch.typing import Protocol, runtime_checkable  # type: ignore
from pipelayer.context import Context
from pipelayer.event_args import FilterEventArgs, PipelineEventArgs


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
class IPipeline(Protocol):  # pragma: no cover
    @property
    def step_start(self) -> IPipelineEventHandlerList:
        pass

    @step_start.setter
    def step_start(self, value: IPipelineEventHandlerList) -> None:
        pass

    @property
    def step_end(self) -> IPipelineEventHandlerList:
        pass

    @step_end.setter
    def step_end(self, value: IPipelineEventHandlerList) -> None:
        pass

    def _on_step_start(self, args: PipelineEventArgs) -> None:
        pass

    def _on_step_end(self, args: PipelineEventArgs) -> None:
        pass


@runtime_checkable
class IFilter(Protocol):  # pragma: no cover
    @property
    def name(self) -> str:
        pass

    @property
    def start(self) -> IFilterEventHandlerList:
        pass

    @start.setter
    def start(self, value: IFilterEventHandlerList) -> None:
        pass

    @property
    def exit(self) -> IFilterEventHandlerList:
        pass

    @exit.setter
    def exit(self, value: IFilterEventHandlerList) -> None:
        pass

    @property
    def end(self) -> IFilterEventHandlerList:
        pass

    @end.setter
    def end(self, value: IFilterEventHandlerList) -> None:
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
PipelineEventHandlerT = TypeVar("PipelineEventHandlerT", bound=Callable[[IPipeline, PipelineEventArgs], None])


class IFilterEventHandlerList(Iterable[FilterEventHandlerT]):  # pragma: no cover

    def append(self, handler: FilterEventHandlerT) -> None:
        pass

    def __iadd__(
        self,
        handlers: Union[
            FilterEventHandlerT,
            Iterable[FilterEventHandlerT]
        ]
    ) -> IFilterEventHandlerList:
        pass

    def __add__(
        self,
        handlers: Union[
            FilterEventHandlerT,
            Iterable[FilterEventHandlerT]
        ]
    ) -> IFilterEventHandlerList:
        pass


class IPipelineEventHandlerList(Iterable[PipelineEventHandlerT]):  # pragma: no cover

    def append(self, handler: PipelineEventHandlerT) -> None:
        pass

    def __iadd__(
        self,
        handlers: Union[
            PipelineEventHandlerT,
            Iterable[PipelineEventHandlerT]
        ]
    ) -> IPipelineEventHandlerList:
        pass

    def __add__(
        self,
        handlers: Union[
            PipelineEventHandlerT,
            Iterable[PipelineEventHandlerT]
        ]
    ) -> IPipelineEventHandlerList:
        pass
