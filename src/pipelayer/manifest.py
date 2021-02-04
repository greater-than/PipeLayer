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
