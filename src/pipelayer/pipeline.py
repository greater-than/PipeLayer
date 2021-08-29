from __future__ import annotations

from typing import Any, Iterable, List, Optional, Tuple, Union, cast

from pipelayer.context import Context
from pipelayer.enum import Action, StepType
from pipelayer.event_args import FilterEventArgs, PipelineEventArgs
from pipelayer.event_decorators import (raise_filter_events,
                                        raise_pipeline_events)
from pipelayer.filter import Filter
from pipelayer.manifest import Manifest, close_manifest, create_manifest
from pipelayer.protocol import (ICompoundStep, IFilter, IStep,
                                PipelineCallableT, PipelineEventHandlerT)
from pipelayer.step import initialize_step


class PipelineEventHandlerList(List[PipelineEventHandlerT]):
    def append(self, handler: PipelineEventHandlerT) -> None:
        super().append(handler)

    def __iadd__(
        self,
        handlers: Union[PipelineEventHandlerT, Iterable[PipelineEventHandlerT]]
    ) -> PipelineEventHandlerList:
        return PipelineEventHandlerList(super().__iadd__(handlers if isinstance(handlers, Iterable) else [handlers]))

    def __add__(
        self,
        handlers: Union[PipelineEventHandlerT, Iterable[PipelineEventHandlerT]]
    ) -> PipelineEventHandlerList:
        return PipelineEventHandlerList(super().__add__(
            PipelineEventHandlerList(handlers)
            if isinstance(handlers, Iterable)
            else PipelineEventHandlerList([handlers])
        ))


class Pipeline(Filter):
    # region Constructors

    def __init__(self: Pipeline,
                 steps: Iterable[Union[IStep, PipelineCallableT]],
                 name: str = "") -> None:
        super().__init__(name or self.__class__.__name__)
        self.__steps: Iterable[Union[IStep, PipelineCallableT]] = steps
        self.__manifest: Optional[Manifest] = None
        self.__exit_pipeline: bool = False
        self.__step_start: PipelineEventHandlerList = PipelineEventHandlerList()
        self.__step_end: PipelineEventHandlerList = PipelineEventHandlerList()
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

    # region Event Handlers

    @property
    def step_start(self) -> PipelineEventHandlerList:
        return self.__step_start

    @property
    def step_end(self) -> PipelineEventHandlerList:
        return self.__step_end

    # endregion

    # endregion
    # region Runners

    def run(self, data: Any = None, context: Optional[Context] = None) -> Any:
        """
        The Pipeline runner
        """
        data, self.__manifest = self._run(data, context or Context())
        return data

    @raise_pipeline_events
    @raise_filter_events
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
    # region Events

    def _on_step_start(self, args: PipelineEventArgs) -> None:
        [e(self, args) for e in self.step_start]

    def _on_step_end(self, args: PipelineEventArgs) -> None:
        [e(self, args) for e in self.step_end]

    # endregion

    # region Event Handlers

    def _handle_exit(self, sender: IFilter, args: FilterEventArgs) -> None:
        self.__exit_pipeline = args.action is Action.EXIT

    # endregion
