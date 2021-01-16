from __future__ import annotations

from typing import Tuple, Type, TypeVar, cast

T = TypeVar("T", bound="Final")


class Final(type):
    """
    Prevents inheritance of any class that sets the __metaclass__ property to Final
    """
    def __new__(cls: Type[T], name: str, bases: Tuple[type, ...], classdict: dict) -> Final:
        for b in bases:
            if isinstance(b, Final):
                raise TypeError("type '{0}' is not an acceptable base type".format(b.__name__))
        return cast(Final, type.__new__(cls, name, bases, dict(classdict)))
