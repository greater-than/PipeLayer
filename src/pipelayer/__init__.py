from __future__ import annotations

import inspect
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

from pipelayer import pipeline
from pipelayer.context import Context
from pipelayer.exception import InvalidFilterException
from pipelayer.filter import Filter
from pipelayer.manifest import (Manifest, ManifestEntry, ManifestEntryList,
                                StepManifestEntry)
from pipelayer.step import Step, StepType


class State(Enum):
    IDLE = 0
    RUNNING = 100
    WAITING = 110
    PAUSED = 120
    COMPLETE = 200
    EXITED = 210
    TERMINATED = 220


class Action(Enum):
    TERMINATE = 0
    RESUME = 1
    PAUSE = 2
    RESTART = 3


class Pipeline:
    # region Constructors

    def __init__(self: Pipeline,
                 steps: List[Union[Step, Callable[[Any, Context], Any]]],
                 name: str = "") -> None:
        self.__name = name or self.__class__.__name__
        self.__steps: List[Union[Step, Callable[[Any, Context], Any]]] = steps
        self.__manifest: Manifest = None  # type: ignore
        self.__state: State = State.IDLE

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError(f"type '{Pipeline.__name__}' is not an acceptable base type")

    # endregion
    # region Properties

    @property
    def name(self) -> str:
        return self.__name

    @property
    def state(self) -> State:
        return self.__state

    @property
    def steps(self) -> List[Union[Step, Callable[[Any, Context], Any]]]:
        return self.__steps

    @property
    def manifest(self) -> Manifest:
        return self.__manifest

    # endregion
    # region Runners

    def run(self, data: Any, context: Optional[Context] = None) -> Any:
        """
        The Pipeline runner
        """
        self.__state = State.RUNNING
        data = self.run_steps(data, context or Context())[0]
        self.__state = State.COMPLETE
        return data

    def run_steps(self, data: Any, context: Context) -> Any:
        self.__initialize_manifest()

        add_to_manifest = self.manifest.steps.append
        create_step_manifest_entry = Pipeline.__create_step_manifest_entry
        close_manifest_entry = Pipeline.__close_manifest_entry
        initialize_step = StepHelper.initialize_step
        run_step_process = Pipeline.__run_step_process

        for step_name, step_type, step_func, pre_process, post_process in map(initialize_step, self.steps):
            manifest_entry = create_step_manifest_entry(step_name, step_type)

            if step_type is StepType.PIPELINE:
                # nested pipeline
                data, manifest_entry.steps = step_func(data, context)
            else:
                # step.pre_process
                data, manifest_entry.pre_process = run_step_process(pre_process, data, context)
                # step
                data = step_func(data, context)
                # step.post_process
                data, manifest_entry.post_process = run_step_process(post_process, data, context)

            close_manifest_entry(manifest_entry)
            add_to_manifest(manifest_entry)

        close_manifest_entry(self.manifest)

        return data, self.manifest

    @staticmethod
    def __run_step_process(
        process: Optional[Callable],
        data: Any,
        context: Optional[Context]
    ) -> Tuple[Any, Optional[ManifestEntry]]:
        """
        The step pre/post process runner
        """
        if not process:
            return data, None

        process_manifest_entry = ManifestEntry(
            name=process.__name__,
            start=datetime.utcnow()
        )

        data = process(data, context)

        process_manifest_entry.end = datetime.utcnow()
        process_manifest_entry.duration = (
            process_manifest_entry.end - process_manifest_entry.start
        )

        return data, process_manifest_entry

    # endregion
    # region Manifest

    def __initialize_manifest(self) -> None:
        if not self.__manifest:
            self.__manifest = Manifest(
                name=self.name,
                start=datetime.utcnow()
            )
        self.manifest.end = None
        self.manifest.duration = None
        self.manifest.steps = ManifestEntryList()

    @staticmethod
    def __create_step_manifest_entry(step_name: str, step_type: StepType) -> StepManifestEntry:
        return StepManifestEntry(
            name=step_name,
            start=datetime.utcnow(),
            step_type=step_type
        )

    @staticmethod
    def __close_manifest_entry(manifest_entry: ManifestEntry) -> None:
        manifest_entry.end = datetime.utcnow()
        manifest_entry.duration = manifest_entry.end - manifest_entry.start

    # endregion


class Switch:
    def __init__(self,
                 expression: Union[Step, Callable[[Any, Context], Any]],
                 cases: Dict[Enum, Union[Step, Callable[[Any, Context], Any]]]) -> None:
        self.__expression = expression
        self.__cases = cases

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError(f"type '{Switch.__name__}' is not an acceptable base type")

    @property
    def expression(self) -> Union[Step, Callable[[Any, Context], Any]]:
        return self.__expression

    @property
    def cases(self) -> Dict[Enum, Union[Step, Callable[[Any, Context], Any]]]:
        return self.__cases

    def run(self, data: Any, context: Context) -> Any:
        step = StepHelper.get_step(self.expression)
        expr_func = StepHelper.get_step_func(step)
        label = next(case for case in self.cases if case is expr_func(data, context))
        case = self.cases[label]
        case_func = StepHelper.get_step_func(case)
        return case_func(data, context)


class StepHelper:

    @staticmethod
    def initialize_step(
        step: Union[Step, Callable[[Any, Context], Any]]
    ) -> Tuple[
        str,
        StepType,
        Callable[[Any, Context], Any],
        Optional[Callable[[Any, Context], Any]],
        Optional[Callable[[Any, Context], Any]],
    ]:
        step = StepHelper.get_step(step)
        step_type = StepHelper.get_step_type(step)
        step_func = StepHelper.get_step_func(step)
        pre, post = StepHelper.get_sub_processes(step)
        return StepHelper.get_step_name(step), step_type, step_func, pre, post

    @staticmethod
    def __is_step_type(step: Union[Step, Callable[[Any, Context], Any]]) -> bool:
        return inspect.isclass(step) and issubclass(cast(type, step), Step)

    @staticmethod
    def __is_run_static(step: Step) -> bool:
        return inspect.getfullargspec(step.run).args[0] != "self"

    @staticmethod
    def get_step(step: Union[Step, Callable[[Any, Context], Any]]) -> Union[Step, Callable[[Any, Context], Any]]:
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
    def get_step_type(step: Union[Step, Callable[[Any, Context], Any]]) -> StepType:
        if isinstance(step, Step):
            return StepType(step.__class__.__name__) if step.__class__.__name__ in StepType else StepType.FILTER
        return StepType.FUNCTION

    @staticmethod
    def get_step_func(step: Union[Step, Callable[[Any, Context], Any]]) -> Callable[[Any, Context], Any]:
        if isinstance(step, Step):
            run_func = step.run_steps if isinstance(step, pipeline.Pipeline) else step.run
            return cast(Callable[[Any, Context], Any], run_func)

        if not StepHelper.__is_callable_valid(cast(Callable, step)):
            raise InvalidFilterException(
                "Step functions must have the same signataure as 'pipelayer.Step.run'"
            )
        return cast(Callable, step)

    @staticmethod
    def get_sub_processes(
        step: Union[Step, Callable[[Any, Context], Any]]
    ) -> Tuple[
        Optional[Callable[[Any, Context], Any]],
        Optional[Callable[[Any, Context], Any]]
    ]:
        return (step.pre_process, step.post_process) if isinstance(step, Filter) else (None, None)

    @staticmethod
    def __is_callable_valid(obj: Callable[..., Any]) -> bool:
        if not obj or not inspect.isfunction(obj):
            return False
        args = inspect.signature(obj).parameters
        return len(args) == 2
