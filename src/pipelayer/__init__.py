from __future__ import annotations

import inspect
from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple, Type, Union

from pipelayer.context import Context
from pipelayer.exception import InvalidFilterException, PipelineException
from pipelayer.filter import Filter
from pipelayer.final import Final
from pipelayer.manifest import (Manifest, ManifestEntry, StepManifestEntry,
                                StepType)
from pipelayer.settings import Settings  # NOQA F401
from pipelayer.step import Step


class Pipeline(Step):
    def __init__(self: Pipeline,
                 steps: List[Union[Step, Callable[[Context, Any], Any]]],
                 name: str = "") -> None:
        super().__init__(name)
        self.__steps: List[Union[Step, Callable[[Context, Any], Any]]] = steps
        self.__manifest: Manifest = None  # type: ignore

    @property
    def steps(self) -> List[Union[Step, Callable[[Context, Any], Any]]]:
        return self.__steps

    @property
    def manifest(self) -> Manifest:
        return self.__manifest

    def run(self, context: Union[Context, Any], data: Any) -> Any:
        """
        The Pipeline runner
        """
        return self.__run_steps(context, data)[0]

    def __run_steps(self, context: Union[Context, Any], data: Any) -> Any:
        self.__initialize_manifest()

        for step in [Pipeline.__initialize_step(step) for step in self.steps]:
            step_name, step_type, step_func, pre_process, post_process = step
            manifest_entry = StepManifestEntry(
                name=step_name,
                start=datetime.utcnow(),
                step_type=step_type
            )

            # pre_process
            data, manifest_entry.pre_process = self.__run_step_process(pre_process, context, data)

            # step
            try:
                if step_type is StepType.PIPELINE:
                    data, manifest_entry.steps = step_func(context, data)
                else:
                    data = step_func(context, data)

            except Exception as e:
                raise PipelineException(inner_exception=e)

            # post_process
            data, manifest_entry.post_process = self.__run_step_process(post_process, context, data)

            manifest_entry.end = datetime.utcnow()
            manifest_entry.duration = manifest_entry.end - manifest_entry.start

            self.manifest.steps.append(manifest_entry)

        end = datetime.utcnow()
        self.manifest.end = end
        self.manifest.duration = end - self.manifest.start

        return data, self.manifest

    def __initialize_manifest(self) -> None:
        if not self.__manifest:
            self.__manifest = Manifest(name=self.name, start=datetime.utcnow())

    @staticmethod
    def __initialize_step(
        step: Union[Step, Type[Filter], Callable[[Context, Any], Any]]
    ) -> Tuple[
        str,
        StepType,
        Callable[[Context, Any], Any],
        Optional[Callable[[Context, Any], Any]],
        Optional[Callable[[Context, Any], Any]],
    ]:
        name = ""
        if inspect.isclass(step):
            # The checks should have isolated the type, but mypy complains
            step = step(step.__name__)  # type: ignore

        if isinstance(step, Step) and issubclass(step.__class__, Step):
            is_filter = issubclass(step.__class__, Filter)
            is_pipeline = isinstance(step, Pipeline)
            step_type = StepType.FILTER if is_filter else StepType.PIPELINE
            func = step.__run_steps if is_pipeline else step.run  # type: ignore
            pre = step.pre_process if is_filter else None  # type: ignore
            post = step.post_process if is_filter else None  # type: ignore
            return step.name, step_type, func, pre, post

        if not Pipeline.__is_callable_valid(step):
            raise InvalidFilterException(
                ("Filter functions cannot be 'None' and must have two arguments.")
            )

        name = (
            f"[{inspect.getsource(step).strip()}]"
            if step.__name__ == "<lambda>"
            else step.__name__
        )

        return name, StepType.FUNCTION, step, None, None

    @staticmethod
    def __is_callable_valid(obj: Callable[..., Any]) -> bool:
        if not obj or not inspect.isfunction(obj):
            return False
        sig = inspect.signature(obj)
        return len(sig.parameters) == 2

    @staticmethod
    def __run_step_process(
        process: Optional[Callable], context: Union[Context, Any], data: Any
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

        try:
            data = process(context, data)
        except Exception as e:
            raise PipelineException(inner_exception=e)

        process_manifest_entry.end = datetime.utcnow()
        process_manifest_entry.duration = (
            process_manifest_entry.end - process_manifest_entry.start
        )

        return data, process_manifest_entry

    __metaclass__ = Final
