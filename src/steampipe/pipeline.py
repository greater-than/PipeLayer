from __future__ import annotations

from copy import deepcopy
from typing import Any, List, Union

from steampipe.context import Context
from steampipe.final import Final
from steampipe.manifest import Manifest
from steampipe.step import Step


class Pipeline:

    __name = ""
    __context: Union[Context, None] = None
    __manifest: Union[Manifest, None] = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def context(self) -> Context:
        if not self.__context:
            raise Exception
        return self.__context

    @property
    def manifest(self) -> Manifest:
        if not self.__manifest:
            self.__manifest = Manifest()
        return self.__manifest

    @classmethod
    def create(cls, context: Context, name: str = "") -> Pipeline:
        pipeline = Pipeline()
        pipeline.__name = name or cls.__name__
        pipeline.__context = context
        pipeline.__manifest = None
        return pipeline

    def run(self, steps: List[Step], data: Any = None) -> Any:
        self.__manifest = None
        self.manifest.add_entry(f"Pipeline start: {self.name}")

        for step in steps:
            try:
                data = deepcopy(data)
            except TypeError:
                raise TypeError("TypeError: data argment cannot be copied")

            self.manifest.add_entry(f"Step start: {step.name}")

            if step.pre_process:
                data = step.pre_process(self.context, data)

            data = step.execute(self.context, data)

            if step.post_process:
                data = step.post_process(self.context, data)

            self.manifest.add_entry(f"Step end: {step.name}")

        self.manifest.add_entry(f"Pipeline end: {self.name}")

        return data

    __metaclass__ = Final
