from datetime import datetime, timedelta
from typing import Callable, Optional

from pipelayer.enum import StepType
from pydantic import BaseModel
from pydantic.json import timedelta_isoformat
from stringbender import camel


class ManifestList(list):
    ...


class Manifest(BaseModel):
    name: str
    step_type: StepType
    start: datetime
    end: Optional[datetime] = None
    duration: Optional[timedelta] = None
    steps: ManifestList = ManifestList()

    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda dt: dt.timestamp(),
            timedelta: timedelta_isoformat,
        }
        allow_population_by_field_name: bool = True
        alias_generator: Callable = camel


def create_manifest(name: str, step_type: StepType) -> Manifest:
    return Manifest(
        name=name,
        step_type=step_type,
        start=datetime.utcnow())


def close_manifest(manifest: Manifest) -> None:
    manifest.end = datetime.utcnow()
    manifest.duration = manifest.end - manifest.start
