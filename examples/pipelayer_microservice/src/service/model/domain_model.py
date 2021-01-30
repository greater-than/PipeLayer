from typing import Callable, List

from pydantic import BaseModel
from stringbender import camel


def to_camel(s: str) -> str:
    return camel(s)


# TODO Add a json encoder to convert model fields to camelCase

class DomainModelConfig:
    allow_population_by_field_name: bool = True
    alias_generator: Callable = to_camel


class DomainModel(BaseModel):
    class Config(DomainModelConfig):
        pass


class DomainModelList(BaseModel):
    __root__: List[BaseModel]
