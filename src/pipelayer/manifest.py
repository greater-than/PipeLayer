from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic.json import timedelta_isoformat


class StepType(Enum):
    PIPELINE = 1
    FILTER = 2
    FUNCTION = 3


class ManifestEntry(BaseModel):
    name: str
    start: datetime
    end: Optional[datetime]
    duration: Optional[timedelta]

    class Config:
        json_encoders = {
            datetime: lambda dt: dt.timestamp(),
            timedelta: timedelta_isoformat,
        }


class ManifestEntryList(list):
    ...


class StepManifestEntry(ManifestEntry):
    step_type: StepType
    steps: Optional[ManifestEntryList]
    pre_process: Optional[ManifestEntry]
    post_process: Optional[ManifestEntry]

    class Config:
        json_encoders = {
            StepType: lambda st: st.name.lower()
        }


class Manifest(ManifestEntry):
    """
    A running log of pipeline activity
    """
    steps: ManifestEntryList = ManifestEntryList()
