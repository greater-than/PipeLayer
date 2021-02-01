from __future__ import annotations

import inspect
from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple, Union, cast

from pipelayer.context import Context
from pipelayer.exception import InvalidFilterException
from pipelayer.filter import Filter
from pipelayer.manifest import (Manifest, ManifestEntry, ManifestEntryList,
                                StepManifestEntry)
from pipelayer.step import Step, StepType


class Pipeline:
    # region Constructors

    def __init__(self: Pipeline,
                 steps: List[Union[Step, Callable[[Any, Context], Any]]],
                 name: str = "") -> None:
        self.__name = name or self.__class__.__name__
        self.__steps: List[Union[Step, Callable[[Any, Context], Any]]] = steps
        self.__manifest: Manifest = None  # type: ignore

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError(f"type '{Pipeline.__name__}' is not an acceptable base type")

    # endregion
    # region Properties

    @property
    def name(self) -> str:
        return self.__name

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
        return self.__run(data, context or Context())[0]

    def __run(self, data: Any, context: Context) -> Any:
        self.__initialize_manifest()

        add_to_manifest = self.manifest.steps.append
        create_step_manifest_entry = Pipeline.__create_step_manifest_entry
        close_manifest_entry = Pipeline.__close_manifest_entry
        initialize_step = Pipeline.__initialize_step
        run_step_process = Pipeline.__run_step_process

        for step_name, step_type, step_func, pre_process, post_process in map(initialize_step, self.steps):
            manifest_entry = create_step_manifest_entry(step_name, step_type)

            # pre_process
            data, manifest_entry.pre_process = run_step_process(pre_process, data, context)

            # step
            if step_type is StepType.PIPELINE:
                data, manifest_entry.steps = step_func(data, context)
            else:
                data = step_func(data, context)

            # post_process
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
    # region Step Initialization

    @staticmethod
    def __initialize_step(
        step: Union[Step, Callable[[Any, Context], Any]]
    ) -> Tuple[
        str,
        StepType,
        Callable[[Any, Context], Any],
        Optional[Callable[[Any, Context], Any]],
        Optional[Callable[[Any, Context], Any]],
    ]:
        if Pipeline.__is_step_type(step) and not Pipeline.__is_run_static(cast(Step, step)):
            step = cast(type, step)()

        step_type = Pipeline.__get_step_type(step)
        step_func = Pipeline.__get_step_func(step)
        pre, post = Pipeline.__get_sub_processes(step)
        return Pipeline.__get_step_name(step), step_type, step_func, pre, post

    @staticmethod
    def __is_step_type(step: Union[Step, Callable[[Any, Context], Any]]) -> bool:
        return inspect.isclass(step) and issubclass(cast(type, step), Step)

    @staticmethod
    def __is_run_static(step: Step) -> bool:
        return inspect.getfullargspec(step.run).args[0] != "self"

    @staticmethod
    def __get_step_name(step: Any) -> str:
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
    def __get_step_type(step: Union[Step, Callable[[Any, Context], Any]]) -> StepType:
        if isinstance(step, Step):
            return StepType.PIPELINE if isinstance(step, Pipeline) else StepType.FILTER
        return StepType.FUNCTION

    @staticmethod
    def __get_step_func(step: Union[Step, Callable[[Any, Context], Any]]) -> Callable[[Any, Context], Any]:
        if isinstance(step, Step):
            run_func = step.__run if isinstance(step, Pipeline) else step.run
            return cast(Callable[[Any, Context], Any], run_func)

        if not Pipeline.__is_callable_valid(cast(Callable, step)):
            raise InvalidFilterException(
                "Step functions must have the same signataure as 'pipelayer.Step.run'"
            )
        return cast(Callable, step)

    @staticmethod
    def __get_sub_processes(
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

    # endregion
