from __future__ import annotations

from enum import Enum
from typing import Any, Callable, List, Optional, Tuple, Union

from pipelayer.context import Context
from pipelayer.manifest import (FilterManifestEntry, Manifest, ManifestEntry,
                                ManifestManager)
from pipelayer.protocol import Step
from pipelayer.step import StepHelper, StepType
from pipelayer.switch import Switch  # NOQA F401


class Pipeline:
    # region Constructors

    def __init__(self: Pipeline,
                 steps: List[Union[Step, Callable[[Any, Context], Any]]],
                 name: str = "") -> None:
        self.__name = name or self.__class__.__name__
        self.__steps: List[Union[Step, Callable[[Any, Context], Any]]] = steps
        self.__manifest: Manifest = None  # type: ignore
        self.__state: Pipeline.State = Pipeline.State.IDLE

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
    # region Runners

    def run(self, data: Any, context: Optional[Context] = None) -> Any:
        """
        The Pipeline runner
        """
        self.__state = Pipeline.State.RUNNING
        data, self.__manifest = self._run_steps(data, context or Context())
        self.__state = Pipeline.State.COMPLETE
        return data

    def _run_steps(self, data: Any, context: Context) -> Tuple[Any, Manifest]:
        manifest = ManifestManager.create_manifest(self.name)

        create_filter_manifest_entry = ManifestManager.create_filter_manifest_entry
        create_manifest = ManifestManager.create_manifest
        close_manifest_entry = ManifestManager.close_manifest_entry
        add_to_manifest = manifest.steps.append
        initialize_step = StepHelper.initialize_step
        run_step_process = Pipeline.__run_step_process

        def yield_data(data: Any, context: Context) -> Any:
            for step_name, step_type, step_func, pre_process, post_process in map(initialize_step, self.steps):

                step_manifest: Union[Manifest, FilterManifestEntry]
                if step_type in (StepType.PIPELINE, StepType.SWITCH):
                    step_manifest = create_manifest(step_name)
                    # nested pipeline
                    data, step_manifest.steps = step_func(data, context)

                else:
                    step_manifest = create_filter_manifest_entry(step_name)
                    # step.pre_process
                    data, step_manifest.pre_process = run_step_process(pre_process, data, context)
                    # step
                    data = step_func(data, context)
                    # step.post_process
                    data, step_manifest.post_process = run_step_process(post_process, data, context)

                close_manifest_entry(step_manifest)
                add_to_manifest(step_manifest)

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

        manifest_entry = ManifestManager.create_manifest_entry(
            name=process.__name__,
            step_type=StepType.FUNCTION
        )

        data = process(data, context)

        ManifestManager.close_manifest_entry(manifest_entry)

        return data, manifest_entry

    # endregion
