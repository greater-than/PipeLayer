from __future__ import annotations

from typing import Any, Callable, List, Optional, Tuple, Union, cast

from pipelayer.context import Context
from pipelayer.enum import Action, StepType
from pipelayer.event_args import FilterEventArgs
from pipelayer.manifest import (FilterManifest, Manifest, ManifestManager,
                                StepManifest)
from pipelayer.protocol import IFilter, IStep
from pipelayer.step import StepHelper
from pipelayer.switch import Switch  # NOQA F401


class Pipeline:
    # region Constructors

    def __init__(self: Pipeline,
                 steps: List[Union[IStep, Callable[[Any, Context], Any]]],
                 name: str = "") -> None:
        self.__name = name or self.__class__.__name__
        self.__steps: List[Union[IStep, Callable[[Any, Context], Any]]] = steps
        self.__manifest: Manifest = None  # type: ignore
        self.__exit_pipeline: bool = False

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError(f"type '{Pipeline.__name__}' is not an acceptable base type")

    # endregion
    # region Properties

    @property
    def name(self) -> str:
        return self.__name

    @property
    def steps(self) -> List[Union[IStep, Callable[[Any, Context], Any]]]:
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
        data, self.__manifest = self._run(data, context or Context())
        return data

    def _run(self, data: Any, context: Context) -> Tuple[Any, Manifest]:
        create_manifest = ManifestManager.create
        close_manifest = ManifestManager.close

        manifest = cast(Manifest, create_manifest(self.name, StepType.PIPELINE))
        add_to_manifest = manifest.steps.append

        initialize_step = StepHelper.initialize_step
        run_step_process = Pipeline.__run_step_process

        for step, step_name, step_type, step_func, pre_process, post_process in map(initialize_step, self.steps):
            step_manifest = create_manifest(step_name, step_type)

            if step_type in (StepType.PIPELINE, StepType.SWITCH):
                data, cast(Manifest, step_manifest).steps = step_func(data, context)

            elif isinstance(step, IFilter):
                # step.pre_process
                data, cast(FilterManifest, step_manifest).pre_process = \
                    run_step_process(pre_process, data, context)

                # step
                step.exit.append(self.__handle_exit)
                data = step_func(data, context)

                if self.__exit_pipeline:
                    close_manifest(step_manifest)
                    add_to_manifest(step_manifest)
                    break

                # step.post_process
                data, cast(FilterManifest, step_manifest).post_process = \
                    run_step_process(post_process, data, context)

            else:
                # step
                data = step_func(data, context)

            close_manifest(step_manifest)
            add_to_manifest(step_manifest)

        close_manifest(manifest)

        return data, manifest

    def __handle_exit(self, sender: IFilter, args: FilterEventArgs) -> None:
        if args.action is Action.EXIT:
            self.__exit_pipeline = True

    @staticmethod
    def __run_step_process(
        process: Optional[Callable],
        data: Any,
        context: Optional[Context]
    ) -> Tuple[Any, Optional[StepManifest]]:
        """
        The step pre/post process runner
        """
        if not process:
            return data, None

        manifest_entry = ManifestManager.create(
            name=process.__name__,
            step_type=StepType.FUNCTION
        )

        data = process(data, context)

        ManifestManager.close(manifest_entry)

        return data, manifest_entry

    # endregion
