from typing import Any, Optional, Protocol

from pydantic import BaseModel

from service.config.app_settings_base import AppSettings


class ISettingsProvider(Protocol):
    def get() -> Any:
        pass


class AppSettingsFactory:
    def create(model: BaseModel, provider: Optional[ISettingsProvider] = None) -> AppSettings:
        return model.parse_obj(provider.get()) if provider else model
