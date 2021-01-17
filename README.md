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
<br>

### Table of Contents

* [Installation](#installation)
* [Quick Start](#quick-start)
* [The Framework](#the-framework)
* [Examples](#examples)
<br><br>

## Installation

From the command line:
```sh
pip install pipelayer
```

## Quick Start

### Step 1: Application Settings
Create a class called AppSettings that inherits from the [`pipelayer.Settings`](Settings) class:

`app_settings.py`
```python
from pipelayer import Settings


class AppSettings(Settings):
    """
    Complete this by adding constants, key/value data from AWS Parameter Store, etc

    The pipelayer.Settings class inherits from pydantic.BaseModel, so fields must be typed appropriately
    """
    ...
```
NOTE: You do not have to use the Settings base class in your application. Any class can be provided.

### Step 2: Application Context
Create a class called AppContext that inherits from the `pipelayer.Context` class:

`app_context.py`
```python
from logging import Logger

from app_settings import AppSettings
from pipelayer import Context


class AppContext(Context):
    def __init__(self, settings: AppSettings, log: Logger = Nones):
        self.__settings = settings
        self.__log = log

    @property
    def settings(self) -> AppSettings:
        return self.__settings

    @property
    def log(self) -> Logger:
        return self.__log
```

### Step 3: Create Pipeline Filters
Create classes that inherits from `pipelayer.Filter`:

`hello_filter.py`
```python
from pipelayer import Filter


class HelloFilter(Filter):
    def run(self, context) -> str:
        return "Hello"
```

`world_filter.py`
```python
from pipelayer import Filter


class WorldFilter(Filter):
    def run(self, context, data) -> str:
        return data + " World!"
```

### Step 4: Create a Pipeline
Create a module to run the pipeline:

`app.py`
```python
from app_context import AppContext
from app_settings import AppSettings
from pipelayer import Pipeline
from hello_filter import HelloFilter
from world_filter import WorldFilter
from logging import Logger

app_settings = AppSettings()
app_context = AppContext(app_settings, Logger("Logger"))
hello_world_pipeline = Pipeline.create(app_context, "Hello World Pipeline")

output = hello_world_pipeline.run([
    HelloFilter(),
    WorldFilter()
])

print(f"Pipeline Output: {output}")
print(hello_world_pipeline.manifest.__dict__)

```

### Step 5: Run the Pipeline
from the command line:
```sh
run app.py
```
---

## The Framework
* [Pipeline](#pipelayer.pipeline)
* [Filter](#pipelayer.filter)
* [Context](#pipelayer.context)
* [Settings](#pipelayer.settings)
* [Manifest](#pipelayer.manifest)
<br><br>


### __`pipelayer.Pipeline`__

***Properties***

__`name`__ (str)<br>
An optional name. It's used in the `Manifest`.

__`context`__ (Context)<br>
An instance of `pipelayer.Context`.

__`manifest`__ (Manifest)<br>
An instance of `pipelayer.Manifest` that is created at runtime.

***Methods***

__`create(context: Context, name: str = "") -> Pipeline`__<br>
The factory method to create a pipeline

__`run(filters: List[Filter], data: Any = None) -> Any`__<br>
The pipeline runner that iterates through the `filters` and pipes filter output to the next filter.
<br><br>


### __`pipelayer.Filter`__
A functional unit that implements the `run` method, and the optional `pre_process` and `post_process` methods.

***Properties***

__`name`__ (str)<br>
Optional. Used by the [`Manifest`](#pipelayer.manifest)

__`pre_process`__ (callable)<br>
Optional.

__`post_process`__ (callable)<br>
Optional.

***Methods***

__`run(context: Context, data: Any) -> Any`__<br>
The type of the `data` argument in the abstract class is `Any`, but you can use the correct type for the data when implementing method. The same is true for the return type.
<br><br>


### __`pipelayer.Context`__
The Context object is used to pass application-level information to each filter.

***Properties***

__[`settings`](#settings)__ (Any)<br>
An optional abstract property for storing application-level data.

__`log`__ (Any)<br>
An optional abstract property for a common logger that can be used within pipeline filters.

__[`manifest`](#manifest)__ (Manifest)<br>
A model that keeps a record of start/stop times for a pipeline, as well as each filter.
<br><br>


### __`pipelayer.Settings`__
The settings class is an optional base class for applications settings that inherits from `pydantic.BaseModel`.
<br><br>


### __`pipelayer.Manifest`__
The Manifest keeps a record of [`Pipeline`](#pipeline) and [`Filter`](#filter) activity.

