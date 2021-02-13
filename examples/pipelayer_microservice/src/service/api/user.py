import json

from pipelayer import Manifest

from service.access_control import authorize
from service.api import handle_exception
from service.config.app_context import AppContext
from service.config.app_settings import DevAppSettings
from service.config.app_settings_factory import AppSettingsFactory
from service.model.domain_model import DomainModel
from service.model.response_model import Response
from service.pipeline.user_pipelines import (find_users_pipeline,
                                             get_user_pipeline,
                                             get_users_pipeline)
from service.provider.user.resreq import ResReqUserProvider

settings = AppSettingsFactory.create(DevAppSettings)
context = AppContext(settings)
user_provider = ResReqUserProvider


def get_response(model: DomainModel, manifest: Manifest) -> dict:
    model = model.__root__ if hasattr(model, "__root__") else model
    resp_model = Response(data=model, manifest=manifest)
    return json.loads(resp_model.json(by_alias=True))


@authorize
def get(**kwargs) -> dict:
    try:
        pipeline = get_user_pipeline(user_provider)
        user = pipeline.run(kwargs, context)
        return get_response(user, pipeline.manifest)
    except Exception as e:
        return handle_exception(e)


@authorize
def get_users(**kwargs) -> dict:
    try:
        pipeline = get_users_pipeline(user_provider)
        users = pipeline.run(kwargs, context)
        return get_response(users, pipeline.manifest)
    except Exception as e:
        return handle_exception(e)


@authorize
def find_users(**kwargs) -> dict:
    try:
        pipeline = find_users_pipeline(context.settings.user_provider)
        users = pipeline.run(kwargs, context)
        return get_response(users, pipeline.manifest)
    except Exception as e:
        return handle_exception(e)
