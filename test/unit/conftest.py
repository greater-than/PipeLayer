from test.fixtures.app_context import AppContext
from test.fixtures.manifest import manifest_dict

import pytest

from pipelayer import Manifest


@pytest.fixture
def app_context() -> AppContext:
    return AppContext()


@pytest.fixture
def manifest() -> dict:
    return Manifest.parse_obj(manifest_dict)
