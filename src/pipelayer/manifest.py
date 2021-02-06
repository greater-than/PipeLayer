from datetime import datetime, timedelta
from typing import Callable, Optional

from pipelayer.step import StepType
from pydantic import BaseModel
from pydantic.json import timedelta_isoformat
from stringbender import camel


class ManifestEntryList(list):
    ...


class ManifestEntry(BaseModel):
    name: str
    step_type: StepType
    start: datetime
    end: Optional[datetime] = None
    duration: Optional[timedelta] = None

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda dt: dt.timestamp(),
            timedelta: timedelta_isoformat,
        }
        allow_population_by_field_name: bool = True
        alias_generator: Callable = camel


class CompoundStepManifestEntry(ManifestEntry):
    steps: ManifestEntryList = ManifestEntryList()


class FilterManifestEntry(CompoundStepManifestEntry):
    step_type: StepType = StepType.FILTER
    pre_process: Optional[ManifestEntry]
    post_process: Optional[ManifestEntry]


class Manifest(CompoundStepManifestEntry):
    """
    A running log of pipeline activity
    """
    step_type: StepType


class ManifestManager:

    @staticmethod
    def create_manifest(name: str, step_type: Optional[StepType] = StepType.PIPELINE) -> Manifest:
        return Manifest(
            name=name,
            step_type=step_type or StepType.PIPELINE,
            start=datetime.utcnow())

    @staticmethod
    def create_filter_manifest_entry(name: str) -> FilterManifestEntry:
        return FilterManifestEntry(
            name=name,
            start=datetime.utcnow())

    @staticmethod
    def create_manifest_entry(name: str, step_type: StepType) -> ManifestEntry:
        return ManifestEntry(
            name=name,
            step_type=step_type,
            start=datetime.utcnow())

    @staticmethod
    def close_manifest_entry(manifest_entry: ManifestEntry) -> None:
        manifest_entry.end = datetime.utcnow()
        manifest_entry.duration = manifest_entry.end - manifest_entry.start
