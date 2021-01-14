from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel
from pydantic.json import timedelta_isoformat


class ManifestEntry(BaseModel):
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    duration: Optional[timedelta]

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),
            timedelta: timedelta_isoformat,
        }


class ManifestEntryList(list):
    ...


class ManifestStep(ManifestEntry):
    pre_process: Optional[ManifestEntry]
    post_process: Optional[ManifestEntry]


class Manifest(ManifestEntry):
    steps: ManifestEntryList = ManifestEntryList()
