from logging import Logger

# =========================================================================
# Remove this patch if running the example outside of the steampipe project
import _path_patch  # noqa F401
# -------------------------------------------------------------------------
from app_context import AppContext
from app_settings import AppSettings
from render import print_manifest
from steampipe import Pipeline
from step.hello_step import HelloStep
from step.world_step import WorldStep


def main() -> None:
    app_settings = AppSettings()

    context = AppContext(app_settings, Logger("Logger"))
    pipeline = Pipeline.create(context, "Hello World Pipeline")
    steps = [
        HelloStep(),
        WorldStep()
    ]
    output = pipeline.run(steps, None)

    print_manifest(pipeline.manifest)

    return output


if __name__ == "__main__":
    from render import print_output
    print_output(main())
