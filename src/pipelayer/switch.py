from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Union, cast
from uuid import uuid4

from pipelayer.context import Context
from pipelayer.enum import StepType
from pipelayer.filter import Filter, raise_events
from pipelayer.manifest import Manifest, close_manifest, create_manifest
from pipelayer.protocol import IStep, PipelineCallableT
from pipelayer.step import (get_step, get_step_func, get_step_name,
                            get_step_type)


class Switch(Filter):
    """
    A Switch/Case filter. It implements the CompoundStep interface.
    """
    # region Constructors

    def __init__(self,
                 expression: Union[IStep, PipelineCallableT],
                 cases: Dict[Any, Union[IStep, PipelineCallableT]],
                 name: Optional[str] = "") -> None:
        """
        Args:
            expression (Union[Step, PipelineCallableT]):
            Can be a class that implements pipelayer.protocol.Step or a function/lambda that
            has the signature (data: Any, context; Context) -> Any.

            cases (Dict[Any, Union[Step, PipelineCallableT]]):
            The list of labels and cases (Step)

            name (Optional[str], optional):
            Used by the Manifest. Defaults to "".
        """
        super().__init__(name or self.__class__.__name__)
        self.__expression = expression
        self.__cases = cases
        self.__manifest: Optional[Manifest] = None
        self.default = uuid4().hex

    def __init_subclass__(cls, **kwargs: Any):
        raise TypeError(f"type '{Switch.__name__}' is not an acceptable base type")

    # endregion
    # region Properties

    @property
    def expression(self) -> Union[IStep, PipelineCallableT]:
        return self.__expression

    @property
    def cases(self) -> Dict[Any, Union[IStep, PipelineCallableT]]:
        return self.__cases

    @property
    def manifest(self) -> Manifest:
        return cast(Manifest, self.__manifest)

    # endregion
    # region Runners

    def run(self, data: Any = None, context: Optional[Context] = None) -> Any:
        """[summary]

        Args:
            data (Any): [description]
            context (Optional[Context], optional): [description]. Defaults to None.

        Returns:
            Any: [description]
        """
        data, self.__manifest = self._run(data, context or Context())
        return data

    @raise_events
    def _run(self, data: Any, context: Context) -> Tuple[Any, Manifest]:

        manifest = create_manifest(get_step_name(self.expression), StepType.SWITCH)

        # Expression
        step = get_step(self.expression)  # type: ignore
        expr_func = get_step_func(step)

        # Eval Expression
        label = next((case for case in self.cases if case == expr_func(data, context)), self.default)

        # Execute Case
        case = self.cases.get(label)
        case_name = "Default"
        case_type = StepType.UNDEFINED
        if case:
            case_func = get_step_func(case)
            case_name = get_step_name(case_func)
            case_type = get_step_type(case_func)

        case_manifest = create_manifest(case_name, case_type)

        data = case_func(data, context) if case else data

        close_manifest(case_manifest)
        manifest.steps.append(case_manifest)

        close_manifest(manifest)
        self.__manifest = manifest

        return data, manifest

    # endregion
