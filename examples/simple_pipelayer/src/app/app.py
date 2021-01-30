# region Imports
# ==========================================================================
# Uncomment this patch if running the example within of the pipelayer project
# import app._path_patch  # NOQA F401

import json
from typing import Any, Tuple

from app.filter.create_response import create_response
from app.filter.hello_filter import HelloFilter
from app.filter.world_filter import WorldFilter
from pipelayer import Pipeline

# endregion


def main() -> Tuple[Pipeline, Any]:
    steps = [
        HelloFilter,
        WorldFilter("Appends: ', World.'", post_process=create_response),
        lambda data, context: json.dumps(data)
    ]
    pipeline = Pipeline(steps, "Hello World Pipeline")
    outer_pipeline = Pipeline([pipeline], "Outer Pipeline")
    output = outer_pipeline.run(None)

    return outer_pipeline, output
