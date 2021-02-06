from __future__ import annotations

from typing import Any, Optional, Protocol, Tuple, runtime_checkable

from pipelayer.context import Context
from pipelayer.manifest import Manifest


@runtime_checkable
class CompoundStep(Protocol):

    @property
    def name(self) -> str:  # pragma: no cover
        raise NotImplementedError

    @property
    def manifest(self) -> Manifest:  # pragma: no cover
        raise NotImplementedError

    def run(self, data: Any, context: Optional[Context]) -> Any:
        raise NotImplementedError

    def _run_steps(self, data: Any, context: Context) -> Tuple[Any, Manifest]:
        raise NotImplementedError
