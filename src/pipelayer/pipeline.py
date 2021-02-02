from typing import Any, Protocol, runtime_checkable

from pipelayer.context import Context


@runtime_checkable
class Pipeline(Protocol):
    def run_steps(self, data: Any, context: Context) -> Any:
        raise NotImplementedError
