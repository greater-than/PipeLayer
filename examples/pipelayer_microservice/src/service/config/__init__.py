from logging import Logger

from pipelayer._patch.typing import Protocol
from service.config.app_settings import AppSettings


class IAppContext(Protocol):
    @property
    def settings(self) -> AppSettings:
        pass

    @property
    def log(self) -> Logger:
        pass
