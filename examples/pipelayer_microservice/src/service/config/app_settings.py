from __future__ import annotations

from pydantic import BaseModel

from service.provider.user.resreq import ResReqUserProvider


class LocalAppSettings(BaseModel):
    user_service_api = "https://reqres.in/api"
    user_provider = ResReqUserProvider


class DevAppSettings:
    user_service_api = "https://reqres.in/api"
    user_provider = ResReqUserProvider


class TestAppSettings:
    user_service_api = "https://reqres.in/api"
    user_provider = ResReqUserProvider


class ProdAppSettings:
    user_service_api = "https://reqres.in/api"
    user_provider = ResReqUserProvider
