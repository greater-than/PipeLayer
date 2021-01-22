# region Imports
# ==========================================================================
# Uncomment this patch if running the example within of the pipelayer project
# import app._path_patch  # NOQA F401

import json
from logging import Logger
from typing import Any, Tuple

from pipelayer import Pipeline

from app.app_context import AppContext
from app.app_settings import AppSettings
from app.filter.create_response import create_response
from app.filter.hello_filter import HelloFilter
from app.filter.world_filter import WorldFilter

# endregion


def main() -> Tuple[Pipeline, Any]:
    app_settings = AppSettings()

    context = AppContext(app_settings, Logger("Logger"))
    pipeline = Pipeline.create(context, "Hello World Pipeline")
    filters = [
        HelloFilter,
        WorldFilter("Append ', World.'", post_process=create_response),
        lambda context, data: json.dumps(data)
    ]
    output = pipeline.run(filters, None)

    return pipeline, output
