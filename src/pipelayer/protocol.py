from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (Any, Callable, List, Optional, Protocol, Tuple,
                    runtime_checkable)

from pipelayer.context import Context
from pipelayer.event_args import EventArgs


@runtime_checkable
class Manifest(Protocol):  # pragma: no cover
    name: str
    step_type: Enum
    steps: List
    start: datetime
    end: Optional[datetime]
    duration: Optional[datetime]


@runtime_checkable
class StepManifest(Protocol):  # pragma: no cover
    name: str
    step_type: Enum
    start: datetime
    end: Optional[datetime]
    duration: Optional[datetime]


@runtime_checkable
class FilterManifest(Protocol):  # pragma: no cover
    name: str
    step_type: Enum
    start: datetime
    end: Optional[datetime]
    duration: Optional[datetime]
    pre_process: Optional[StepManifest]
    post_process: Optional[StepManifest]


@runtime_checkable
class Step(Protocol):  # pragma: no cover
    def run(self, data: Any, context: Optional[Context]) -> Any:
        pass


@runtime_checkable
class Filter(Protocol):  # pragma: no cover
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
    def start(self) -> List[Callable[[Filter, Any], Any]]:
        pass

    @property
    def exit(self) -> List[Callable[[Filter, Any], Any]]:
        pass

    @property
    def end(self) -> List[Callable[[Filter, Any], Any]]:
        pass

    def run(self, data: Any, context: Any) -> Any:
        pass

    def _on_start(self, args: EventArgs) -> None:
        pass

    def _on_exit(self, args: EventArgs) -> None:
        pass

    def _on_end(self, args: EventArgs) -> None:
        pass


@runtime_checkable
class CompoundStep(Protocol):  # pragma: no cover

    @property
    def name(self) -> str:
        pass

    @property
    def manifest(self) -> Manifest:
        pass

    def run(self, data: Any, context: Any) -> Any:
        pass

    def _run(self, data: Any, context: Any) -> Tuple[Any, Manifest]:
        pass
