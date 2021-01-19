from logging import Logger
from typing import Any, Tuple

from pipelayer import Pipeline

# =========================================================================
# Remove this patch if running the example outside of the pipelayer project
import app._path_patch  # NOQA F401
from app.app_context import AppContext
from app.app_settings import AppSettings
from app.filter.hello_filter import HelloFilter
from app.filter.world_filter import WorldFilter
from app.render import print_manifest


def main() -> Tuple[Pipeline, Any]:
    app_settings = AppSettings()

    context = AppContext(app_settings, Logger("Logger"))
    pipeline = Pipeline.create(context, "Hello World Pipeline")
    filters = [HelloFilter(), WorldFilter()]
    output = pipeline.run(filters, None)

    print_manifest(pipeline.manifest)

    return pipeline, output


if __name__ == "__main__":
    from app.render import print_output
    print_output(main())
