# PipeLayer
PipeLayer is a lightweight pipeline framework. Define a series of filters, and chain them together to create modular applications.

```python
from app_context import AppContext
from app_settings import AppSettings
from pipelayer import Pipeline
from hello_filter import HelloFilter
from world_filter import WorldFilter
from logging import Logger

app_settings = AppSettings()
app_context = AppContext(app_settings, Logger("Logger"))
pipeline = Pipeline.create(app_context, "Hello World Pipeline")

output = pipeline.run([
    HelloFilter(),
    WorldFilter()
])

print(f"Pipeline Output: {output}")
print(pipeline.manifest.__dict__)
```

See the package [README](src/README.md) for complete documentation and implementation steps.

## Examples

* [Simple Pipeline](examples/simple_pipelayer/README.md)

## License
The license can be [found here](LICENSE)
