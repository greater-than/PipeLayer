from enum import Enum, EnumMeta
from typing import Any


class EnumContains(EnumMeta):
    def __contains__(cls, item: Any) -> bool:
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True


class Event(Enum, metaclass=EnumContains):
    START = "start"
    EXIT = "exit"
    END = "end"


class State(Enum, metaclass=EnumContains):
    RUNNING = 1
    SKIPPING = 2
    EXITING = 3
    COMPLETING = 4


class Action(Enum, metaclass=EnumContains):
    CONTINUE = 1  # CARRY ON
    SKIP = 2      # SKIPS THE CURRENT FILTER
    EXIT = 3      # EXITS THE PIPELINE


class StepType(Enum, metaclass=EnumContains):
    PIPELINE = "Pipeline"
    SWITCH = "Switch"
    FILTER = "Filter"
    FUNCTION = "Function"
