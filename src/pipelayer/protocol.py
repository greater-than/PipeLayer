from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (Any, Callable, List, Optional, Protocol, Tuple,
                    runtime_checkable)

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
class IStepManifest(Protocol):  # pragma: no cover
    name: str
    step_type: Enum
    start: datetime
    end: Optional[datetime]
    duration: Optional[datetime]


@runtime_checkable
class IFilterManifest(Protocol):  # pragma: no cover
    name: str
    step_type: Enum
    start: datetime
    end: Optional[datetime]
    duration: Optional[datetime]
    pre_process: Optional[IStepManifest]
    post_process: Optional[IStepManifest]


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
    def pre_process(self) -> Optional[Callable]:
        pass

    @property
    def post_process(self) -> Optional[Callable]:
        pass

    @property
    def start(self) -> List[Callable[[IFilter, Any], Any]]:
        pass

    @property
    def exit(self) -> List[Callable[[IFilter, Any], Any]]:
        pass

    @property
    def end(self) -> List[Callable[[IFilter, Any], Any]]:
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
