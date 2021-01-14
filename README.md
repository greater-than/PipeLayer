# SteamPipe
Steampipe is a lightweight pipeline framework. Define a series of reusable steps, and chain them together to create modular applications.

```python
from app_context import AppContext
from app_settings import AppSettings
from steampipe.pipeline import Pipeline
from hello_step import HelloStep
from world_step import WorldStep
from logging import Logger

app_settings = AppSettings()
app_context = AppContext(app_settings, Logger("Logger"))
pipeline = Pipeline.create(app_context, "Hello World Pipeline")

output = pipeline.run([
    HelloStep(),
    WorldStep()
])

print(f"Pipeline Output: {output}")
print(pipeline.manifest.__dict__)
```

See the package [README](./src/steampipe/README.md) for complete documentation and implementation steps.

## Examples

* [Simple Pipeline](./examples/simple_pipeline/README.md)

## License
The license can be [found here](./LICENSE)
