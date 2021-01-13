from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel


class ManifestEntry(BaseModel):
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    duration: Optional[timedelta]


class ManifestEntryList(list):
    ...


class ManifestStep(ManifestEntry):
    pre_process: Optional[ManifestEntry]
    post_process: Optional[ManifestEntry]


class Manifest(ManifestEntry):
    steps: ManifestEntryList = ManifestEntryList()
