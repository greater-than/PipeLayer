from __future__ import annotations

from enum import Enum

from pipelayer.enum_meta import EnumContains


class StepType(Enum, metaclass=EnumContains):
    PIPELINE = "Pipeline"
    SWITCH = "Switch"
    FILTER = "Filter"
    FUNCTION = "Function"
