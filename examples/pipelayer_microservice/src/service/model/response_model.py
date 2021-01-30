from typing import Union

from pipelayer.manifest import Manifest

from service.model.domain_model import DomainModel, DomainModelList


class Response(DomainModel):
    data: Union[DomainModel, DomainModelList]
    manifest: Manifest
