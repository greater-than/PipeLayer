from logging import Logger

from app_context import AppContext
from app_settings import AppSettings
from steampipe.pipeline import Pipeline
from step.hello_step import HelloStep
from step.world_step import WorldStep

app_settings = AppSettings()
app_context = AppContext(app_settings, Logger("Logger"))
hello_world_pipeline = Pipeline.create(app_context, "Hello World Pipeline")

output = hello_world_pipeline.run([
    HelloStep(),
    WorldStep()
])

print(f"Pipeline Output: {output}")
print(hello_world_pipeline.manifest.__dict__)
