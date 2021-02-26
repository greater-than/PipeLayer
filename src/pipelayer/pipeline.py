from __future__ import annotations

from typing import Any, Iterable, Optional, Tuple, Union, cast

from pipelayer.context import Context
from pipelayer.enum import Action, StepType
from pipelayer.event_args import FilterEventArgs
from pipelayer.filter import Filter, raise_events
from pipelayer.manifest import Manifest, close_manifest, create_manifest
from pipelayer.protocol import ICompoundStep, IFilter, IStep, PipelineCallableT
from pipelayer.step import initialize_step


class Pipeline(Filter):
    # region Constructors

    def __init__(self: Pipeline,
                 steps: Iterable[Union[IStep, PipelineCallableT]],
                 name: str = "") -> None:
        super().__init__(name or self.__class__.__name__)
        self.__steps: Iterable[Union[IStep, PipelineCallableT]] = steps
        self.__manifest: Optional[Manifest] = None
        self.__exit_pipeline: bool = False
        self.exit += self._handle_exit

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError(f"type '{Pipeline.__name__}' is not an acceptable base type")

    # endregion
    # region Properties

    @property
    def steps(self) -> Iterable[Union[IStep, PipelineCallableT]]:
        return self.__steps

    @property
    def manifest(self) -> Manifest:
        return cast(Manifest, self.__manifest)

    # endregion
    # region Runners

    def run(self, data: Any = None, context: Optional[Context] = None) -> Any:
        """
        The Pipeline runner
        """
        data, self.__manifest = self._run(data, context or Context())
        return data

    @raise_events
    def _run(self, data: Any, context: Context) -> Tuple[Any, Manifest]:

        manifest = create_manifest(self.name, StepType.PIPELINE)

        for s, s_name, s_type, s_func in map(initialize_step, self.steps):  # type: ignore

            s_manifest = create_manifest(s_name, s_type)

            if isinstance(s, IFilter):
                s.exit += self._handle_exit

                if isinstance(s, ICompoundStep):
                    data, m_fest = s_func(data, context)
                    s_manifest.steps = cast(Manifest, m_fest).steps
                else:
                    data = s_func(data, context)

                if self.__exit_pipeline:
                    close_manifest(s_manifest)
                    manifest.steps.append(s_manifest)
                    break

            else:
                data = s_func(data, context)

            close_manifest(s_manifest)
            manifest.steps.append(s_manifest)

        close_manifest(manifest)

        return data, manifest

    # endregion
    # region Event Handlers

    def _handle_exit(self, sender: IFilter, args: FilterEventArgs) -> None:
        self.__exit_pipeline = args.action is Action.EXIT

    # endregion
