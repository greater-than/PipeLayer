from __future__ import annotations

import inspect
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, cast

from pipelayer.compound_step import CompoundStep
from pipelayer.context import Context
from pipelayer.exception import InvalidFilterException
from pipelayer.filter import Filter
from pipelayer.manifest import FilterManifestEntry, Manifest, ManifestEntry
from pipelayer.step import Step, StepType

# region Enums


class State(Enum):
    IDLE = 0
    RUNNING = 1
    WAITING = 2
    PAUSED = 3
    EXITED = 4
    TERMINATED = 5
    COMPLETE = 6


class Action(Enum):
    TERMINATE = 0
    RESUME = 1
    PAUSE = 2
    RESTART = 3

# endregion


class Pipeline:
    # region Constructors

    def __init__(self: Pipeline,
                 steps: List[Union[Step, Callable[[Any, Context], Any]]],
                 name: str = "") -> None:
        self.__name = name or self.__class__.__name__
        self.__steps: List[Union[Step, Callable[[Any, Context], Any]]] = steps
        self.__manifest: ManifestEntry = None  # type: ignore
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
    def manifest(self) -> ManifestEntry:
        return self.__manifest

    # endregion
    # region Runners

    def run(self, data: Any, context: Optional[Context] = None) -> Any:
        """
        The Pipeline runner
        """
        self.__state = State.RUNNING
        data, self.__manifest = self.run_steps(data, context or Context())
        self.__state = State.COMPLETE
        return data

    def run_steps(self, data: Any, context: Context) -> Tuple[Any, ManifestEntry]:
        manifest = ManifestHelper.create_manifest(self.name)

        create_filter_manifest_entry = ManifestHelper.create_filter_manifest_entry
        create_manifest = ManifestHelper.create_manifest
        close_manifest_entry = ManifestHelper.close_manifest_entry
        add_to_manifest = manifest.steps.append
        initialize_step = StepHelper.initialize_step
        run_step_process = Pipeline.__run_step_process

        def yield_data(data: Any, context: Context) -> Any:
            for step_name, step_type, step_func, pre_process, post_process in map(initialize_step, self.steps):

                manifest_entry: Union[Manifest, FilterManifestEntry]
                if step_type in (StepType.PIPELINE, StepType.SWITCH):
                    manifest_entry = create_manifest(step_name)
                    # nested pipeline
                    data, manifest_entry.steps = step_func(data, context)

                else:
                    manifest_entry = create_filter_manifest_entry(step_name)
                    # step.pre_process
                    data, manifest_entry.pre_process = run_step_process(pre_process, data, context)
                    # step
                    data = step_func(data, context)
                    # step.post_process
                    data, manifest_entry.post_process = run_step_process(post_process, data, context)

                close_manifest_entry(manifest_entry)
                add_to_manifest(manifest_entry)

            yield data

        data = yield_data(data, context)

        close_manifest_entry(manifest)

        return next(data), manifest

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

        manifest_entry = ManifestHelper.create_manifest_entry(
            name=process.__name__,
            step_type=StepType.FUNCTION
        )

        data = process(data, context)

        manifest_entry.end = datetime.utcnow()
        manifest_entry.duration = (
            manifest_entry.end - manifest_entry.start
        )

        return data, manifest_entry

    # endregion


class Switch:
    # region Constructors
    def __init__(self,
                 expression: Union[Step, Callable[[Any, Context], Any]],
                 cases: Dict[Enum, Union[Step, Callable[[Any, Context], Any]]]) -> None:
        self.__expression = expression
        self.__cases = cases
        self.__manifest: Manifest = None  # type: ignore

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError(f"type '{Switch.__name__}' is not an acceptable base type")

    # endregion
    # region Properties

    @property
    def expression(self) -> Union[Step, Callable[[Any, Context], Any]]:
        return self.__expression

    @property
    def cases(self) -> Dict[Enum, Union[Step, Callable[[Any, Context], Any]]]:
        return self.__cases

    @property
    def manifest(self) -> Manifest:
        return self.__manifest

    # endregion
    # region Runners

    def run(self, data: Any, context: Optional[Context] = None) -> Any:
        """[summary]

        Args:
            data (Any): [description]
            context (Optional[Context], optional): [description]. Defaults to None.

        Returns:
            Any: [description]
        """
        data, self.__manifest = self.run_steps(data, context or Context())
        return data

    def run_steps(self, data: Any, context: Context) -> Tuple[Any, Manifest]:
        manifest = ManifestHelper.create_manifest(
            StepHelper.get_step_name(self.expression),
            StepType.SWITCH
        )

        # Expression
        step = StepHelper.get_step(self.expression)
        expr_func = StepHelper.get_step_func(step)

        # Eval Expression
        label = next(case for case in self.cases if case is expr_func(data, context))

        # Execute Case
        case = self.cases[label]
        case_func = StepHelper.get_step_func(case)
        case_manifest_entry = ManifestHelper.create_manifest_entry(
            StepHelper.get_step_name(case_func),
            StepType.FUNCTION  # TODO This could be any StepType
        )

        data = case_func(data, context)

        ManifestHelper.close_manifest_entry(case_manifest_entry)
        manifest.steps.append(case_manifest_entry)

        ManifestHelper.close_manifest_entry(manifest)
        self.__manifest = manifest

        return data, manifest

    # endregion


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
            run_func = step.run_steps if isinstance(step, CompoundStep) else step.run
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
    def __is_step_type(step: Union[Step, Callable[[Any, Context], Any]]) -> bool:
        return inspect.isclass(step) and issubclass(cast(type, step), Step)

    @staticmethod
    def __is_run_static(step: Step) -> bool:
        return inspect.getfullargspec(step.run).args[0] != "self"

    @staticmethod
    def __is_callable_valid(obj: Callable[..., Any]) -> bool:
        if not obj or not inspect.isfunction(obj):
            return False
        args = inspect.signature(obj).parameters
        return len(args) == 2


class ManifestHelper:

    @staticmethod
    def create_manifest(name: str, step_type: Optional[StepType] = StepType.PIPELINE) -> Manifest:
        return Manifest(
            name=name,
            step_type=step_type or StepType.PIPELINE,
            start=datetime.utcnow())

    @staticmethod
    def create_filter_manifest_entry(name: str) -> FilterManifestEntry:
        return FilterManifestEntry(
            name=name,
            start=datetime.utcnow())

    @staticmethod
    def create_manifest_entry(name: str, step_type: StepType) -> ManifestEntry:
        return ManifestEntry(
            name=name,
            step_type=step_type,
            start=datetime.utcnow())

    @staticmethod
    def close_manifest_entry(manifest_entry: ManifestEntry) -> None:
        manifest_entry.end = datetime.utcnow()
        manifest_entry.duration = manifest_entry.end - manifest_entry.start
