import json
from typing import List, Union

from pipelayer import Manifest

from service.access_control import authorize
from service.api import handle_exception
from service.config import context
from service.model.domain_model import DomainModel
from service.model.response_model import Response
from service.pipeline.user_pipelines import (find_users_pipeline,
                                             get_user_pipeline,
                                             get_users_pipeline)


def get_response(model: Union[DomainModel, List[DomainModel]], manifest: Manifest) -> dict:
    resp_model = Response(data=model, manifest=manifest)
    return json.loads(resp_model.json())


@authorize
def get(**kwargs) -> dict:
    try:
        user = get_user_pipeline.run(kwargs, context)
        return get_response(user, get_user_pipeline.manifest)
    except Exception as e:
        return handle_exception(e)


@authorize
def get_users(**kwargs) -> dict:
    try:
        users = get_users_pipeline.run(kwargs, context)
        return get_response(users, get_users_pipeline.manifest)
    except Exception as e:
        return handle_exception(e)


@authorize
def find_users(**kwargs) -> dict:
    try:
        users = find_users_pipeline.run(kwargs, context)
        return get_response(users, get_user_pipeline.manifest)
    except Exception as e:
        return handle_exception(e)
