from copy import deepcopy
from typing import Any, List

from steampipe.context import Context
from steampipe.final import Final
from steampipe.step import Step


class Pipeline:
    def __init__(self, context: Context, name: str = "") -> None:
        self.__name = name
        self.__context = context

    @property
    def context(self) -> Context:
        return self.__context

    def run(self, steps: List[Step], data: Any) -> Any:
        self.context.log.info(f"Run Pipeline: {self.__name}")

        for step in steps:
            try:
                data = deepcopy(data)
            except Exception as e:  # TODO what exception is raised?
                raise e

            if step.pre_process:
                data = step.pre_process(self.context, data)

            data = step.execute(self.context, data)

            if step.post_process:
                data = step.post_process(self.context, data)

        return data

    __metaclass__ = Final
