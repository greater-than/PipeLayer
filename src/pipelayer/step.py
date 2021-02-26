from __future__ import annotations

import inspect
from typing import Any, Callable, Tuple, Union, cast

from pipelayer.context import Context
from pipelayer.enum import StepType
from pipelayer.exception import InvalidFilterException
from pipelayer.protocol import ICompoundStep, IStep, PipelineCallableT


class _StepProxy:
    def __init__(self, func: PipelineCallableT) -> None:
        if not func or not is_callable_valid(cast(Callable, func)):
            raise InvalidFilterException(
                "Step functions must have the same signataure as 'pipelayer.Step.run'"
            )
        self.__func = func
        self.__name = ""

    @property
    def name(self) -> str:
        if not self.__name:
            self.__name = get_step_name(self.__func)
        return self.__name

    def run(self, data: Any, context: Context) -> Any:
        return self.__func(data, context)


def initialize_step(
    step: Union[IStep, PipelineCallableT]
) -> Tuple[
    Union[IStep, PipelineCallableT],
    str,
    StepType,
    PipelineCallableT
]:
    step = get_step(step)
    step_name = get_step_name(step)
    step_type = get_step_type(step)
    step_func: PipelineCallableT = get_step_func(step)
    return step, step_name, step_type, step_func


def get_step(step: Union[IStep, PipelineCallableT]) -> Union[IStep, PipelineCallableT]:
    if is_step_type(step):
        return cast(type, step)()
    if not isinstance(step, IStep):
        step = cast(IStep, _StepProxy(step))
    return step


def get_step_func(step: Union[IStep, PipelineCallableT]) -> PipelineCallableT:
    if is_step(step):
        run_func = cast(ICompoundStep, step)._run if is_compound_step(step) else cast(IStep, step).run
        return cast(PipelineCallableT, run_func)

    return cast(PipelineCallableT, step)


def get_step_name(step: Any) -> str:
    if hasattr(step, "name") and step.name:
        step_name = step.name
        return step_name

    if is_step(step):
        return cast(type, step).__name__ if inspect.isclass(step) else step.__class__.__name__

    return (
        f"<{inspect.getsource(step).strip()}>"
        if step.__name__ == "<lambda>"
        else step.__name__
    )


def get_step_type(step: Union[IStep, PipelineCallableT]) -> StepType:
    if is_proxy(step):
        return StepType.FUNCTION
    if is_step(step):
        return StepType(step.__class__.__name__) if step.__class__.__name__ in StepType else StepType.FILTER
    return StepType.FUNCTION


def is_step_type(step: Union[IStep, PipelineCallableT]) -> bool:
    return inspect.isclass(step) and issubclass(cast(type, step), IStep)


def is_class_func_static(class_type: type, func_name: str = "run") -> bool:
    func = getattr(class_type, func_name)
    for cls in inspect.getmro(class_type):
        if inspect.isroutine(func) \
                and func.__name__ in cls.__dict__ \
                and isinstance(cls.__dict__[func.__name__], staticmethod):
            return True
    return False


def is_callable_valid(obj: Callable[..., Any]) -> bool:
    if not obj or not inspect.isfunction(obj):
        return False
    args = inspect.signature(obj).parameters
    return len(args) == 2


def is_proxy(obj: Any) -> bool:
    return isinstance(obj, _StepProxy)


def is_step(obj: Any) -> bool:
    return isinstance(obj, IStep)


def is_compound_step(obj: Any) -> bool:
    return isinstance(obj, ICompoundStep)
