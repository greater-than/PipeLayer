from typing import Callable, List

from pydantic import BaseModel
from stringbender import camel


class DomainModelConfig:
    populate_by_name: bool = True
    alias_generator: Callable = camel


class DomainModel(BaseModel):
    class ConfigDict(DomainModelConfig):
        pass


class DomainModelList(BaseModel):
    __root__: List[BaseModel]
