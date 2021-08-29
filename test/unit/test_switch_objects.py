from __future__ import annotations

from typing import Any

import pytest
from pipelayer import Switch


class AnObject:
    name = "NAMES"


class AnotherObject:
    label = "LABEL"


class ObjectFactory:
    def create(data, context) -> Any:
        if data == 1:
            return AnObject()
        else:
            return AnotherObject()


obj_switch = Switch(
    ObjectFactory.create, {
        AnObject():
            lambda d, c: {"object": str(type(d))},
        AnotherObject():
            lambda d, c: {"object": str(type(d))}
    }
)


@pytest.mark.unit
class TestSwitchCompareObjects:

    @pytest.mark.happy
    def test_switch_with_objects(self):
        assert True
