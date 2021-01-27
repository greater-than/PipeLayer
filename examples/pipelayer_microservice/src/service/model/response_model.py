from typing import List, Union

from pipelayer.manifest import Manifest
from service.model.domain_model import DomainModel


class Response(DomainModel):
    data: Union[DomainModel, List[DomainModel]]
    manifest: Manifest
