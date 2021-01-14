from test.fixtures.app_context import AppContext
from test.fixtures.app_settings import AppSettings

import pytest


@pytest.fixture
def app_settings() -> AppSettings:
    return AppSettings()


@pytest.fixture
def app_context(app_settings) -> AppContext:
    return AppContext(app_settings)
