from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, List

from steampipe.context import Context
from steampipe.final import Final
from steampipe.manifest import Manifest, ManifestEntry, ManifestStep
from steampipe.step import Step


class Pipeline:

    __name = ""
    __context: Context
    __manifest: Manifest

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
            self.__manifest = Manifest(name=self.name)
        return self.__manifest

    @classmethod
    def create(cls, context: Context, name: str = "") -> Pipeline:
        pipeline = Pipeline()
        pipeline.__name = name or cls.__name__
        pipeline.__context = context
        return pipeline

    def run(self, steps: List[Step], data: Any = None) -> Any:
        self.__manifest = Manifest(name=self.name)
        self.manifest.start = datetime.utcnow()

        for step in steps:
            manifest_step = ManifestStep(
                name=step.name,
                start=datetime.utcnow()
            )

            if step.pre_process:
                data = self._run_step_process(
                    self.context,
                    manifest_step,
                    step.pre_process,
                    data
                )

            data = step.execute(self.context, data)

            if step.post_process:
                data = self._run_step_process(
                    self.context,
                    manifest_step,
                    step.post_process,
                    data,
                    False
                )

            manifest_step.end = datetime.utcnow()
            manifest_step.duration = (manifest_step.end - manifest_step.end)
            self.manifest.steps.append(manifest_step)

        self.manifest.end = datetime.utcnow()
        self.manifest.duration = (self.manifest.end - self.manifest.start)

        return data

    @staticmethod
    def _run_step_process(context: Context, manifest_step: ManifestStep, process: Callable,
                          data: Any, pre_process: bool = True) -> Any:

        step_process = ManifestEntry(
            name=process.__name__,
            start=datetime.utcnow()
        )
        data = process(context, data)
        step_process.end = datetime.utcnow()

        if pre_process:
            manifest_step.pre_process = step_process
        else:
            manifest_step.post_process = step_process
        return data

    __metaclass__ = Final
