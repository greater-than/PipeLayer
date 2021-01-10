from abc import ABC
from logging import Logger

from steampipe.settings import Settings


class Context(ABC):
    def __init__(self, settings: Settings, log: Logger):
        self.__settings = settings
        self.__log = log

    @property
    def settings(self) -> Settings:
        return self.__settings

    @property
    def log(self) -> Logger:
        return self.__log
