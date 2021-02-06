from __future__ import annotations

from typing import Any, Optional, Protocol, runtime_checkable

from pipelayer.context import Context


@runtime_checkable
class Step(Protocol):
    def run(self, data: Any, context: Optional[Context]) -> Any:
        raise NotImplementedError
