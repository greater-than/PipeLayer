from logging import Logger

# =========================================================================
# Remove this patch if running the example outside of the pipelayer project
import _path_patch  # noqa F401
# -------------------------------------------------------------------------
from app_context import AppContext
from app_settings import AppSettings
from filter.hello_filter import HelloFilter
from filter.world_filter import WorldFilter
from pipelayer import Pipeline
from render import print_manifest


def main() -> None:
    app_settings = AppSettings()

    context = AppContext(app_settings, Logger("Logger"))
    pipeline = Pipeline.create(context, "Hello World Pipeline")
    filters = [
        HelloFilter(),
        WorldFilter()
    ]
    output = pipeline.run(filters, None)

    print_manifest(pipeline.manifest)

    return output


if __name__ == "__main__":
    from render import print_output
    print_output(main())
