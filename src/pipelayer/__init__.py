from __future__ import annotations

import inspect
from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple, Type, Union

from pipelayer.context import Context
from pipelayer.exception import InvalidFilterException, PipelineException
from pipelayer.filter import Filter
from pipelayer.final import Final
from pipelayer.manifest import FilterManifestEntry, Manifest, ManifestEntry
from pipelayer.settings import Settings  # NOQA F401


class Pipeline:
    __name: str
    __context: Union[Context, Any]
    __manifest: Manifest

    @property
    def name(self) -> str:
        return self.__name

    @property
    def context(self) -> Union[Context, Any]:
        return self.__context

    @property
    def manifest(self) -> Manifest:
        return self.__manifest

    @classmethod
    def create(cls, context: Union[Context, Any], name: str = "") -> Pipeline:
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

        for filter in [Pipeline.__initialize_filter(filter) for filter in filters]:
            filter_name, filter_func, pre_process, post_process = filter

            manifest_entry = FilterManifestEntry(name=filter_name, start=datetime.utcnow())

            # pre_process
            try:
                manifest_entry.pre_process, data = self.__run_filter_process(pre_process, data)
            except Exception as e:
                raise PipelineException(inner_exception=e)

            # filter
            try:
                data = filter_func(self.context, data)
            except Exception as e:
                raise PipelineException(inner_exception=e)

            # post_process
            try:
                manifest_entry.post_process, data = self.__run_filter_process(post_process, data)
            except Exception as e:
                raise PipelineException(inner_exception=e)

            manifest_entry.end = datetime.utcnow()
            manifest_entry.duration = (manifest_entry.end - manifest_entry.start)

            self.manifest.filters.append(manifest_entry)

        end = datetime.utcnow()
        self.manifest.end = end
        self.manifest.duration = (end - self.manifest.start)

        return data

    @staticmethod
    def __initialize_filter(filter: Union[Filter, Type[Filter], Callable[[Context, Any], Any]]) -> Tuple[
        str,
        Callable[[Context, Any], Any],
        Optional[Callable[[Context, Any], Any]],
        Optional[Callable[[Context, Any], Any]]
    ]:
        name = ""
        if inspect.isclass(filter):
            # The checks should have isolated the type, but mypy complains
            filter = filter(filter.__name__)  # type: ignore

        if isinstance(filter, Filter) and issubclass(filter.__class__, Filter):
            return filter.name, filter.run, filter.pre_process, filter.post_process

        if not Pipeline.__is_callable_valid(filter):
            raise InvalidFilterException(("Filter functions cannot be 'None' and must have two arguments."))

        name = f"[{inspect.getsource(filter).strip()}]" if filter.__name__ == "<lambda>" else filter.__name__

        return name, filter, None, None

    @staticmethod
    def __is_callable_valid(obj: Callable[..., Any]) -> bool:
        if not obj or not inspect.isfunction(obj):
            return False
        sig = inspect.signature(obj)
        return len(sig.parameters) == 2

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
