from datetime import datetime, timedelta
from typing import Callable, Optional

from pipelayer.step import StepType
from pydantic import BaseModel
from pydantic.json import timedelta_isoformat
from stringbender import camel


def to_camel(s: str) -> str:
    return camel(s)


class ManifestEntry(BaseModel):
    name: str
    start: datetime
    end: Optional[datetime]
    duration: Optional[timedelta]

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda dt: dt.timestamp(),
            timedelta: timedelta_isoformat,
        }
        allow_population_by_field_name: bool = True
        alias_generator: Callable = to_camel


class ManifestEntryList(list):
    ...


class StepManifestEntry(ManifestEntry):
    step_type: StepType
    steps: Optional[ManifestEntryList]
    pre_process: Optional[ManifestEntry]
    post_process: Optional[ManifestEntry]


class Manifest(ManifestEntry):
    """
    A running log of pipeline activity
    """
    steps: ManifestEntryList = ManifestEntryList()
