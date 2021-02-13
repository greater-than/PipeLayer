from __future__ import annotations

from typing import Any

from pipelayer.context import Context
from pipelayer.enum import Action, State


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
