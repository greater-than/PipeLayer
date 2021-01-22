from test.fixtures.app_context import AppContext
from test.fixtures.app_settings import AppSettings
from test.fixtures.manifest import manifest_dict

import pytest
from pipelayer import Manifest


@pytest.fixture
def app_settings() -> AppSettings:
    return AppSettings()


@pytest.fixture
def app_context(app_settings) -> AppContext:
    return AppContext(app_settings)


@pytest.fixture
def manifest() -> dict:
    return Manifest.parse_obj(manifest_dict)
