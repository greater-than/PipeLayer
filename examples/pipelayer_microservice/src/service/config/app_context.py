from __future__ import annotations

from logging import DEBUG, Logger, getLogger
from typing import Optional

from pipelayer import Context
from service.config.app_settings_base import AppSettings

debug_logger = getLogger("Debug Logger")
debug_logger.setLevel(DEBUG)


class AppContext(Context):
    def __init__(self, settings: AppSettings, log: Optional[Logger] = debug_logger) -> None:
        self.__settings = settings
        self.__log = log

    @property
    def settings(self) -> AppSettings:
        return self.__settings

    @property
    def log(self) -> Logger:
        return self.__log
