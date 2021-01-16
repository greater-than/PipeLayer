from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel
from pydantic.json import timedelta_isoformat


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


class FilterManifestEntry(ManifestEntry):
    pre_process: Optional[ManifestEntry]
    post_process: Optional[ManifestEntry]


class ManifestEntryList(list):
    ...


class Manifest(ManifestEntry):
    """
    A running log of pipeline activity
    """
    filters: ManifestEntryList = ManifestEntryList()
