# SteamPipe Documentation
Steampipe is a lightweight pipeline framework. Define a series of steps, and chain them together to create plug-and-play applications.

## Table of Contents
* [Getting Started](#getting-started)
    * [Installation](#installation)
    * [Quick Start](#quick-start)
* [The Pipeline](#the-pipeline)
* [The Pipeline Context](#the-pipeline-context)
* [Application Settings](#application-settings)
* [The Pipeline Manifest](#the-pipeline-manifest)
* [Steps](steps)

## Getting Started

### Installation

From the command line:
```sh
pip install steampipe
```

### Quick Start

### Application Settings
Create a class called AppSettings that inherits from the Steampipe Settings class:

`app_settings.py`
```python
from steampipe.settings import Settings


class AppSettings(Settings):
    """
    Complete this by adding constants, key/value data from AWS Parameter Store, etc

    NOTE: The Settings class inherits from pydantic.BaseModel, so fields must be typed appropriately
    """
    ...
```

### Application Context
Create a class called AppContext that inherits from the SteamPipe Context class:

`app_context.py`
```python
from logging import Logger

from app_settings import AppSettings
from steampipe.context import Context


class AppContext(Context):
    def __init__(self, settings: AppSettings, log: Logger):
        self.__settings = settings
        self.__log = log

    @property
    def settings(self) -> AppSettings:
        return self.__settings

    @property
    def log(self) -> Logger:
        return self.__log
```

### Create Pipeline Steps
Create a class that inherits from SteamPipe Step:

`hello_step.py`
```python
from steampipe.step import Step


class HelloStep(Step):

    def execute(self, context) -> str:
        return "Hello"
```

`world_step.py`
```python
from steampipe.step import Step


class WorldStep(Step):

    def execute(self, context, data) -> str:
        return data + "World"
```




### Create a Pipeline
Create a module to run the pipeline:

`app.py`
```python
from app_context import AppContext
from app_settings import AppSettings
from steampipe.pipeline import Pipeline
from hello_step import HelloStep
from world_step import WorldStep
from logging import Logger

app_settings = AppSettings()
app_context = AppContext(app_settings, Logger("Logger"))
hello_world_pipeline = Pipeline.create(app_context, "Hello World Pipeline")

output = hello_world_pipeline.run([
    HelloStep(),
    WorldStep()
])

print(f"Pipeline Output: {output}")
print(hello_world_pipeline.manifest.__dict__)

```
### Run the Pipeline
from the command line:
```sh
run app.py
```

### The Pipeline Context
The Context object is used to pass application-level information to each step. The Context class contains two abstract properties `settings` and `log`.

* `settings` is where you can store application-level data.
* `log` is a logger, by default it uses the built-in Python Logger
* `manifest` is an ordered dictionary that keeps a record of start/stop times for a pipeline, as well as each step.



### Steps
Create a class that inherits from `steampipe.Step` abstract class, and implements the execute method.

```
from steampipe import Context, Step


class MyStep(Step):
    def execute(context: Context, data: Any) -> Any:
        ...
```

The type of the `data` argument in the abstract class is `Any`, but you can use the correct type for the data in this method. The same is true for the return type.