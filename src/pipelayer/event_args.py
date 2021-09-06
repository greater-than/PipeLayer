from __future__ import annotations

from typing import Any

from pipelayer.context import Context
from pipelayer.enum import Action, State
from pipelayer.manifest import Manifest


class PipelineEventArgs:
    def __init__(
        self, step_name: str, data: Any, manifest_entry: Manifest
    ) -> None:
        self.__step_name: str = step_name
        self.data: Any = data
        self.__manifest_entry: Manifest = manifest_entry

    @property
    def step_name(self) -> str:
        return self.__step_name

    @property
    def manifest_entry(self) -> Manifest:
        return self.__manifest_entry


class FilterEventArgs:
    def __init__(
        self, data: Any, context: Context, state: State
    ) -> None:
        self.data: Any = data
        self.__context = context
        self.state: State = state
        self.action: Action = Action.CONTINUE

    @property
    def context(self) -> Context:
        return self.__context
