
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, List

from pipelayer.context import Context
from pipelayer.filter import Filter
from pipelayer.final import Final
from pipelayer.manifest import FilterManifestEntry, Manifest, ManifestEntry
from pipelayer.settings import Settings  # noqa F401


class Pipeline:

    __name: str
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
        """
        Pipeline factory
        """
        pipeline = Pipeline()
        pipeline.__name = name or cls.__name__
        pipeline.__context = context
        return pipeline

    def run(self, filters: List[Filter], data: Any = None) -> Any:
        """
        The Pipeline runner.
        """
        self.__manifest = Manifest(name=self.name)
        self.manifest.start = datetime.utcnow()

        for filter in filters:
            manifest_filter = FilterManifestEntry(
                name=filter.name,
                start=datetime.utcnow()
            )

            if filter.pre_process:
                data = self._run_filter_process(
                    self.context,
                    manifest_filter,
                    filter.pre_process,
                    data
                )

            data = filter.run(self.context, data)

            if filter.post_process:
                data = self._run_filter_process(
                    self.context,
                    manifest_filter,
                    filter.post_process,
                    data,
                    False
                )

            manifest_filter.end = datetime.utcnow()
            manifest_filter.duration = (manifest_filter.end - manifest_filter.end)
            self.manifest.filters.append(manifest_filter)

        self.manifest.end = datetime.utcnow()
        self.manifest.duration = (self.manifest.end - self.manifest.start)

        return data

    @staticmethod
    def _run_filter_process(context: Context, filter_manifest_entry: FilterManifestEntry, process: Callable,
                            data: Any, pre_process: bool = True) -> Any:

        filter_process = ManifestEntry(
            name=process.__name__,
            start=datetime.utcnow()
        )
        data = process(context, data)
        filter_process.end = datetime.utcnow()

        if pre_process:
            filter_manifest_entry.pre_process = filter_process
        else:
            filter_manifest_entry.post_process = filter_process
        return data

    __metaclass__ = Final
