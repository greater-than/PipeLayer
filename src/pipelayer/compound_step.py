from __future__ import annotations

from typing import Any, Protocol, Tuple, runtime_checkable

from pipelayer.context import Context
from pipelayer.manifest import Manifest, ManifestEntry


@runtime_checkable
class CompoundStep(Protocol):
    def run_steps(self, data: Any, context: Context) -> Tuple[Any, ManifestEntry]:
        raise NotImplementedError

    @property
    def manifest(self) -> Manifest:  # pragma: no cover
        raise NotImplementedError
