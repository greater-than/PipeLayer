from typing import Callable, List

from pydantic import BaseModel
from stringbender import camel


class DomainModelConfig:
    allow_population_by_field_name: bool = True
    alias_generator: Callable = camel


class DomainModel(BaseModel):
    class Config(DomainModelConfig):
        pass


class DomainModelList(BaseModel):
    __root__: List[BaseModel]
