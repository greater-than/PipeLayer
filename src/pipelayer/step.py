from __future__ import annotations

import inspect
from enum import Enum
from typing import Any, Callable, Optional, Tuple, Type, Union, cast

from pipelayer.enum_meta import EnumContains
from pipelayer.exception import InvalidFilterException
from pipelayer.protocol import CompoundStep, Filter, Step


class StepType(Enum, metaclass=EnumContains):
    PIPELINE = "Pipeline"
    SWITCH = "Switch"
    FILTER = "Filter"
    FUNCTION = "Function"


class StepHelper:

    @staticmethod
    def initialize_step(
        step: Union[Step, Callable[[Any, Any], Any]]
    ) -> Tuple[
        str,
        StepType,
        Callable[[Any, Any], Any],
        Optional[Callable[[Any, Any], Any]],
        Optional[Callable[[Any, Any], Any]],
    ]:
        step = StepHelper.get_step(step)
        step_type = StepHelper.get_step_type(step)
        step_func = StepHelper.get_step_func(step)
        pre, post = StepHelper.get_sub_processes(step)
        return StepHelper.get_step_name(step), step_type, step_func, pre, post

    @staticmethod
    def get_step(step: Union[Step, Callable[[Any, Any], Any]]) -> Union[Step, Callable[[Any, Any], Any]]:
        if StepHelper.__is_step_type(step) and not StepHelper.__is_run_static(cast(Step, step)):
            return cast(type, step)()
        return step

    @staticmethod
    def get_step_name(step: Any) -> str:
        if hasattr(step, "name") and step.name:
            return step.name

        if isinstance(step, Step):
            return cast(type, step).__name__ if inspect.isclass(step) else step.__class__.__name__

        return (
            f"<{inspect.getsource(step).strip()}>"
            if step.__name__ == "<lambda>"
            else step.__name__
        )

    @staticmethod
    def get_step_type(step: Union[Step, Callable[[Any, Any], Any]]) -> StepType:
        if isinstance(step, Step):
            return StepType(step.__class__.__name__) if step.__class__.__name__ in StepType else StepType.FILTER
        return StepType.FUNCTION

    @staticmethod
    def get_step_func(step: Union[Step, Callable[[Any, Any], Any]]) -> Callable[[Any, Any], Any]:
        if isinstance(step, Step):
            run_func = step._run_steps if isinstance(step, CompoundStep) else step.run
            return cast(Callable[[Any, Any], Any], run_func)

        if not StepHelper.__is_callable_valid(cast(Callable, step)):
            raise InvalidFilterException(
                "Step functions must have the same signataure as 'pipelayer.Step.run'"
            )
        return cast(Callable, step)

    @staticmethod
    def get_sub_processes(
        step: Union[Step, Callable[[Any, Any], Any]]
    ) -> Tuple[
        Optional[Callable[[Any, Any], Any]],
        Optional[Callable[[Any, Any], Any]]
    ]:
        return (step.pre_process, step.post_process) if isinstance(step, Filter) else (None, None)

    @staticmethod
    def __is_step_type(step: Union[Step, Callable[[Any, Any], Any]]) -> bool:
        return inspect.isclass(step) and issubclass(cast(type, step), Step)

    @staticmethod
    def __is_run_static(step: Step) -> bool:
        for cls in inspect.getmro(cast(Type, step)):
            if inspect.isroutine(step.run) \
                    and step.run.__name__ in cls.__dict__ \
                    and isinstance(cls.__dict__[step.run.__name__], staticmethod):
                return True
        return False

    @staticmethod
    def __is_callable_valid(obj: Callable[..., Any]) -> bool:
        if not obj or not inspect.isfunction(obj):
            return False
        args = inspect.signature(obj).parameters
        return len(args) == 2
