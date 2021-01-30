from logging import Logger
from typing import Any

from pipelayer import Context

from service.config.app_settings import AppSettings


class AppContext(Context):
    def __init__(self, settings: AppSettings, log: Logger):
        self.__settings = settings
        self.__log = log
        self.__request = None

    @property
    def settings(self) -> AppSettings:
        return self.__settings

    @property
    def log(self) -> Logger:
        return self.__log

    @property
    def request(self) -> Any:
        return self.__request

    @request.setter
    def request(self, value: Any):
        self.__request = value
