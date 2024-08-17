from datetime import datetime, timedelta
from typing import Callable, List, Optional

from pipelayer.enum import StepType
from pipelayer.utils.datetime_utils import get_now_utc
from pydantic import BaseModel, dataclasses
from pydantic.json import timedelta_isoformat
from stringbender import camel


class Config:
    arbitrary_types_allowed = True


@dataclasses.dataclass
class ManifestList(list):
    ...


class Manifest(BaseModel):
    name: str
    step_type: StepType
    start: datetime
    end: Optional[datetime] = None
    duration: Optional[timedelta] = None
    steps: List = list()

    class ConfigDict:
        use_enum_values = True
        json_encoders = {
            datetime: lambda dt: dt.timestamp(),
            timedelta: timedelta_isoformat,
        }
        populate_by_name: bool = True
        alias_generator: Callable = camel


def create_manifest(name: str, step_type: StepType) -> Manifest:
    return Manifest(
        name=name,
        step_type=step_type,
        start=get_now_utc())


def close_manifest(manifest: Manifest) -> None:
    manifest.end = get_now_utc()
    manifest.duration = manifest.end - manifest.start
