from typing import Any, Optional

from pipelayer._patch.typing import Protocol

from service.config.app_settings import AppSettings


class ISettingsProvider(Protocol):
    def get(*args) -> Any:
        pass


def create(provider: Optional[ISettingsProvider] = None) -> AppSettings:
    return AppSettings.model_validate(provider.get()) if provider else AppSettings()
