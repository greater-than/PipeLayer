
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, List, Optional

from pipelayer.context import Context
from pipelayer.filter import Filter
from pipelayer.final import Final
from pipelayer.manifest import FilterManifestEntry, Manifest, ManifestEntry
from pipelayer.settings import Settings  # NOQA F401


class Pipeline:

    __name: str
    __context: Context
    __manifest: Manifest

    @property
    def name(self) -> str:
        return self.__name

    @property
    def context(self) -> Context:
        return self.__context

    @property
    def manifest(self) -> Manifest:
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
        The Pipeline runner
        """
        self.__manifest = Manifest(name=self.name, start=datetime.utcnow())

        for filter in filters:
            manifest_entry = FilterManifestEntry(name=filter.name, start=datetime.utcnow())

            # pre_process
            data = Pipeline.__run_filter_process(self.context, manifest_entry, filter.pre_process, data)

            # filter
            data = filter.run(self.context, data)

            # post_process
            data = Pipeline.__run_filter_process(self.context, manifest_entry, filter.post_process, data, False)

            manifest_entry.end = datetime.utcnow()
            manifest_entry.duration = (manifest_entry.end - manifest_entry.start)

            self.manifest.filters.append(manifest_entry)

        end = datetime.utcnow()
        self.manifest.end = end
        self.manifest.duration = (end - self.manifest.start)

        return data

    @staticmethod
    def __run_filter_process(context: Context, filter_manifest_entry: FilterManifestEntry,
                             process: Optional[Callable], data: Any, pre_process: bool = True) -> Any:
        """
        The filter pre/post process runner
        """
        if not process:
            return data

        process_manifest_entry = ManifestEntry(name=process.__name__, start=datetime.utcnow())

        data = process(context, data)

        process_manifest_entry.end = datetime.utcnow()
        process_manifest_entry.duration = (process_manifest_entry.end - process_manifest_entry.start)

        if pre_process:
            filter_manifest_entry.pre_process = process_manifest_entry
        else:
            filter_manifest_entry.post_process = process_manifest_entry
        return data

    __metaclass__ = Final
