import datetime as d
from datetime import datetime, timedelta
from typing import Callable, List, Optional

from pipelayer.enum import StepType
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
        start=datetime.now(d.UTC))  # type: ignore


def close_manifest(manifest: Manifest) -> None:
    manifest.end = datetime.now(d.UTC)  # type: ignore
    manifest.duration = manifest.end - manifest.start
