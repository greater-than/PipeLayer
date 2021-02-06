from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from pipelayer.context import Context
from pipelayer.filter import Filter  # NOQA F401
from pipelayer.manifest import (FilterManifestEntry, Manifest, ManifestEntry,
                                ManifestManager)
from pipelayer.protocol import Step
from pipelayer.step import StepHelper, StepType


class Pipeline:
    # region Constructors

    def __init__(self: Pipeline,
                 steps: List[Union[Step, Callable[[Any, Context], Any]]],
                 name: str = "") -> None:
        self.__name = name or self.__class__.__name__
        self.__steps: List[Union[Step, Callable[[Any, Context], Any]]] = steps
        self.__manifest: ManifestEntry = None  # type: ignore
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
    def manifest(self) -> ManifestEntry:
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


class Switch:
    # region Constructors

    def __init__(self,
                 expression: Union[Step, Callable[[Any, Context], Any]],
                 cases: Dict[Enum, Union[Step, Callable[[Any, Context], Any]]],
                 name: Optional[str] = "") -> None:
        self.__expression = expression
        self.__cases = cases
        self.__manifest: Manifest = None  # type: ignore
        self.__name = name or self.__class__.__name__

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError(f"type '{Switch.__name__}' is not an acceptable base type")

    # endregion
    # region Properties

    @property
    def name(self) -> str:
        return self.__name

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
        data, self.__manifest = self._run_steps(data, context or Context())
        return data

    def _run_steps(self, data: Any, context: Context) -> Tuple[Any, Manifest]:

        get_step = StepHelper.get_step
        get_step_name = StepHelper.get_step_name
        get_step_type = StepHelper.get_step_type
        get_step_func = StepHelper.get_step_func

        manifest = ManifestManager.create_manifest(
            StepHelper.get_step_name(self.expression),
            StepType.SWITCH
        )

        # Expression
        step = get_step(self.expression)
        expr_func = get_step_func(step)

        # Eval Expression
        label = next(case for case in self.cases if case is expr_func(data, context))

        # Execute Case
        case = self.cases[label]
        case_func = get_step_func(case)
        case_manifest_entry = ManifestManager.create_manifest_entry(
            get_step_name(case_func),
            get_step_type(case_func)
        )
        data = case_func(data, context)

        ManifestManager.close_manifest_entry(case_manifest_entry)
        manifest.steps.append(case_manifest_entry)

        ManifestManager.close_manifest_entry(manifest)
        self.__manifest = manifest

        return data, manifest

    # endregion
