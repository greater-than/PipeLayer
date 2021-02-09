from __future__ import annotations

from typing import Any

from pipelayer.context import Context
from pipelayer.enum import Action, State


class EventArgs:
    def __init__(
        self: EventArgs, data: Any, context: Context, state: State
    ) -> None:
        self.__data = data
        self.__context = context
        self.__state = state
        self.__action = Action.CONTINUE

    @property
    def data(self) -> Any:
        return self.__data

    @data.setter
    def data(self, value: Any) -> None:
        self.__data = value

    @property
    def context(self) -> Context:
        return self.__context

    @property
    def action(self) -> Any:
        return self.__action

    @action.setter
    def action(self, value: Action) -> None:
        self.__action = value

    @property
    def state(self) -> State:
        return self.__state

    @state.setter
    def state(self, value: State) -> None:
        self.__state == value
