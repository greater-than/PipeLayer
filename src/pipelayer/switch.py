from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple, Union

from pipelayer.context import Context
from pipelayer.manifest import Manifest, ManifestManager
from pipelayer.protocol import Step
from pipelayer.step import StepHelper, StepType


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
