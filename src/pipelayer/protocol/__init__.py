from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import (Any, Callable, List, Optional, Protocol, Tuple,
                    runtime_checkable)

from pipelayer.context import Context


@runtime_checkable
class Manifest(Protocol):  # pragma: no cover
    name: str
    step_type: Enum
    steps: List
    start: datetime
    end: Optional[datetime]
    duration: Optional[datetime]


@runtime_checkable
class Step(Protocol):  # pragma: no cover
    def run(self, data: Any, context: Optional[Context]) -> Any:
        raise NotImplementedError


@runtime_checkable
class Filter(Protocol):  # pragma: no cover
    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def pre_process(self) -> Optional[Callable]:
        raise NotImplementedError

    @property
    def post_process(self) -> Optional[Callable]:
        raise NotImplementedError

    def run(self, data: Any, context: Any) -> Any:
        raise NotImplementedError


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

    def _run_steps(self, data: Any, context: Any) -> Tuple[Any, Manifest]:
        pass
