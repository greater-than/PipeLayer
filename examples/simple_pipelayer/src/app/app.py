# =========================================================================
# Remove this patch if running the example outside of the pipelayer project
from logging import Logger
from typing import Any, Tuple

from pipelayer import Pipeline
from pipelayer.manifest import Manifest

import app._path_patch  # NOQA F401
from app.app_context import AppContext
from app.app_settings import AppSettings
from app.filter.create_response import create_response
from app.filter.hello_filter import HelloFilter
from app.filter.world_filter import WorldFilter


def main() -> Tuple[Manifest, Any]:
    app_settings = AppSettings()

    context = AppContext(app_settings, Logger("Logger"))
    pipeline = Pipeline.create(context, "Hello World")
    filters = [
        HelloFilter,
        WorldFilter(post_process=create_response)
    ]
    output = pipeline.run(filters, None)

    return pipeline.manifest, output
