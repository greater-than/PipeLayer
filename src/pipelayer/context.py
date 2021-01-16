from abc import ABC, abstractmethod
from typing import Any


class Context(ABC):
    """
    A extensible container with abstract properties for settings and a logger.
    """

    @property
    @abstractmethod
    def settings(self) -> Any:
        """
        A container for application level settings
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def log(self) -> Any:
        """
        A container for a Logger
        """
        raise NotImplementedError
