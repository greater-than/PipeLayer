from __future__ import annotations

import inspect
from typing import Any, Callable, Optional, Tuple, Union, cast

from pipelayer.context import Context
from pipelayer.enum import StepType
from pipelayer.exception import InvalidFilterException
from pipelayer.protocol import ICompoundStep, IFilter, IStep


class _StepProxy:
    def __init__(self, func: Callable[[Any, Optional[Any]], Any]) -> None:
        if not func or not StepHelper.is_callable_valid(cast(Callable, func)):
            raise InvalidFilterException(
                "Step functions must have the same signataure as 'pipelayer.Step.run'"
            )
        self.__func = func
        self.__name = ""

    @property
    def name(self) -> str:
        if not self.__name:
            self.__name = StepHelper.get_step_name(self.__func)
        return self.__name

    def run(self, data: Any, context: Context) -> Any:
        return self.__func(data, context)


class StepHelper:

    @staticmethod
    def initialize_step(
        step: Union[IStep, Callable[[Any, Any], Any]]
    ) -> Tuple[
        Union[IFilter, IStep, Callable[[Any, Any], Any]],
        str,
        StepType,
        Callable[[Any, Any], Any],
        Optional[Callable[[Any, Any], Any]],
        Optional[Callable[[Any, Any], Any]],
    ]:
        step = StepHelper.get_step(step)
        step_name = StepHelper.get_step_name(step)
        step_type = StepHelper.get_step_type(step)
        step_func = StepHelper.get_step_func(step)
        pre, post = StepHelper.get_sub_processes(step)
        return step, step_name, step_type, step_func, pre, post

    @staticmethod
    def get_step(step: Union[IStep, Callable[[Any, Any], Any]]) -> IStep:
        if StepHelper.__is_step_type(step):
            return cast(type, step)()
        if not isinstance(step, IStep):
            step = cast(IStep, _StepProxy(step))
        return step

    @staticmethod
    def get_step_func(step: Union[IStep, Callable[[Any, Any], Any]]) -> Callable[[Any, Any], Any]:
        if StepHelper.is_step(step):
            run_func = cast(ICompoundStep, step)._run if StepHelper.is_compound_step(step) else cast(IStep, step).run
            return cast(Callable[[Any, Any], Any], run_func)

        return cast(Callable, step)

    @staticmethod
    def get_step_name(step: Any) -> str:
        if hasattr(step, "name") and step.name:
            step_name = step.name
            return step_name

        if StepHelper.is_step(step):
            return cast(type, step).__name__ if inspect.isclass(step) else step.__class__.__name__

        return (
            f"<{inspect.getsource(step).strip()}>"
            if step.__name__ == "<lambda>"
            else step.__name__
        )

    @staticmethod
    def get_step_type(step: Union[IStep, Callable[[Any, Any], Any]]) -> StepType:
        if StepHelper.is_proxy(step):
            return StepType.FUNCTION
        if StepHelper.is_filter(step):
            return StepType.FILTER
        if StepHelper.is_step(step):
            return StepType(step.__class__.__name__) if step.__class__.__name__ in StepType else StepType.FILTER
        return StepType.FUNCTION

    @staticmethod
    def get_sub_processes(
        step: Union[IStep, Callable[[Any, Any], Any]]
    ) -> Tuple[
        Optional[Callable[[Any, Any], Any]],
        Optional[Callable[[Any, Any], Any]]
    ]:

        return (cast(IFilter, step).pre_process, cast(IFilter, step).post_process) \
            if StepHelper.is_filter(step) \
            else (None, None)

    @staticmethod
    def __is_step_type(step: Union[IStep, Callable[[Any, Any], Any]]) -> bool:
        return inspect.isclass(step) and issubclass(cast(type, step), IStep)

    @staticmethod
    def __is_class_func_static(class_type: type, func_name: str = "run") -> bool:
        func = getattr(class_type, func_name)
        for cls in inspect.getmro(class_type):
            if inspect.isroutine(func) \
                    and func.__name__ in cls.__dict__ \
                    and isinstance(cls.__dict__[func.__name__], staticmethod):
                return True
        return False

    @staticmethod
    def is_callable_valid(obj: Callable[..., Any]) -> bool:
        if not obj or not inspect.isfunction(obj):
            return False
        args = inspect.signature(obj).parameters
        return len(args) == 2

    @staticmethod
    def is_proxy(obj: Any) -> bool:
        return isinstance(obj, _StepProxy)

    @staticmethod
    def is_filter(obj: Any) -> bool:
        return isinstance(obj, IFilter)

    @staticmethod
    def is_step(obj: Any) -> bool:
        return isinstance(obj, IStep)

    @staticmethod
    def is_compound_step(obj: Any) -> bool:
        return isinstance(obj, ICompoundStep)
