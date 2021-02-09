from datetime import datetime, timedelta
from typing import Callable, Optional, Union

from pipelayer.enum import StepType
from pydantic import BaseModel
from pydantic.json import timedelta_isoformat
from stringbender import camel


class ManifestList(list):
    ...


class StepManifest(BaseModel):
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


class _CompoundStepManifest(StepManifest):
    steps: ManifestList = ManifestList()


class FilterManifest(_CompoundStepManifest):
    step_type: StepType = StepType.FILTER
    pre_process: Optional[StepManifest]
    post_process: Optional[StepManifest]


class Manifest(_CompoundStepManifest):
    """
    A running log of pipeline activity
    """
    pass


class ManifestManager:

    @staticmethod
    def create(name: str, step_type: StepType) -> Union[Manifest, FilterManifest, StepManifest]:
        if step_type is StepType.FILTER:
            return FilterManifest(
                name=name,
                step_type=StepType.FILTER,
                start=datetime.utcnow())

        if step_type is StepType.SWITCH:
            return Manifest(
                name=name,
                step_type=StepType.SWITCH,
                start=datetime.utcnow())

        if step_type is StepType.FUNCTION:
            return StepManifest(
                name=name,
                step_type=StepType.FUNCTION,
                start=datetime.utcnow())

        return Manifest(
            name=name,
            step_type=StepType.PIPELINE,
            start=datetime.utcnow())

    @staticmethod
    def close(manifest: StepManifest) -> None:
        manifest.end = datetime.utcnow()
        manifest.duration = manifest.end - manifest.start
