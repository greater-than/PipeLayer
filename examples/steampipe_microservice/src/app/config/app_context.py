from logging import Logger

from app.config.app_settings import AppSettings
from steampipe.context import Context


class AppContext(Context):
    def __init__(self, settings: AppSettings, log: Logger):
        self.__settings = settings
        self.__log = log

    @property
    def settings(self) -> AppSettings:
        return self.__settings

    @property
    def log(self) -> Logger:
        return self.__log
