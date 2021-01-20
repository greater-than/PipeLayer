
from __future__ import annotations

import inspect
from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple, Type, Union

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

    def run(self, filters: List[Union[Filter, Callable[[Context, Any], Any]]], data: Any = None) -> Any:
        """
        The Pipeline runner
        """
        self.__manifest = Manifest(name=self.name, start=datetime.utcnow())

        for filter in filters:
            filter_name = filter.name if isinstance(filter, Filter) else ""
            manifest_entry = FilterManifestEntry(name=filter_name, start=datetime.utcnow())

            # initialize
            filter_func, pre_process, post_process = self.__initialize_filter(filter)

            # pre_process
            manifest_entry.pre_process, data = self.__run_filter_process(pre_process, data)

            # filter
            data = filter_func(self.context, data)

            # post_process
            manifest_entry.post_process, data = self.__run_filter_process(post_process, data)

            manifest_entry.end = datetime.utcnow()
            manifest_entry.duration = (manifest_entry.end - manifest_entry.start)

            self.manifest.filters.append(manifest_entry)

        end = datetime.utcnow()
        self.manifest.end = end
        self.manifest.duration = (end - self.manifest.start)

        return data

    @staticmethod
    def __initialize_filter(filter: Union[Filter, Type[Filter], Callable[[Context, Any], Any]]) -> Tuple[
        Callable[[Context, Any], Any],
        Optional[Callable[[Context, Any], Any]],
        Optional[Callable[[Context, Any], Any]]
    ]:
        if inspect.isclass(filter) and issubclass(type(filter), Filter):
            # The checks should have isolated the type, but mypy complains
            filter = filter()  # type: ignore

        if isinstance(filter, Filter):
            return filter.run, filter.pre_process, filter.post_process

        func = filter if inspect.isfunction(filter) else lambda context, data: data

        return func, None, None

    def __run_filter_process(self, process: Optional[Callable], data: Any) -> Tuple[Optional[ManifestEntry], Any]:
        """
        The filter pre/post process runner
        """
        if not process:
            return None, data

        process_manifest_entry = ManifestEntry(name=process.__name__, start=datetime.utcnow())

        data = process(self.context, data)

        process_manifest_entry.end = datetime.utcnow()
        process_manifest_entry.duration = (process_manifest_entry.end - process_manifest_entry.start)

        return process_manifest_entry, data

    __metaclass__ = Final
