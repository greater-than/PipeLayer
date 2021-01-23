# PipeLayer
PipeLayer is a lightweight Python pipeline framework. Define a series of steps, and chain them together to create modular applications.
<br>

### Table of Contents

* [Installation](#installation)
* [Getting Started](#getting-started)
* [The Framework](#the-framework)
<br><br>

## Installation

From the command line:
```sh
pip install pipelayer
```

## Getting Started

### Step 1: Application Settings
Create a class called AppSettings that inherits from [`pipelayer.Settings`](#pipelayersettings):

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

`hello_world_filters.py`
```python
from pipelayer import Filter


class HelloFilter(Filter):
    def run(self, context) -> str:
        return "Hello"


class WorldFilter(Filter):
    def run(self, context, data) -> str:
        return f"{data},  World!"
```

`functions.py`
```python
def create_message_dict(context, data: str) -> dict:
    return {"message": data}
```

### Step 4: Create a Pipeline
Create a module to run the pipeline:

`app.py`
```python
from logging import Logger
from pipelayer import Pipeline

from app_context import AppContext
from app_settings import AppSettings
from functions import create_message
from hello_world_filters import HelloFilter, WorldFilter

app_settings = AppSettings()
app_context = AppContext(app_settings, Logger("Logger"))
hello_world_pipeline = Pipeline.create(app_context, "Hello World Pipeline")

output = hello_world_pipeline.run([
    HelloFilter,                           # pipeline.Filter type
    WorldFilter(),                         # pipeline.Filter instance
    create_message_dict                    # function type
    lambda context, data: json.dumps(data) # anonymous function
])

# output = '{"message": "Hello, World!"}'

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
* [Pipeline](#pipelayerpipeline)
* [Filter](#pipelayerfilter)
* [Context](#pipelayercontext)
* [Settings](#pipelayersettings)
* [Manifest](#pipelayermanifest)
* [Utilities](#utilities)
<br><br>


### __`pipelayer.Pipeline(`[`Step`](#pipelayerstep)`)`__

***Constructor***

__`__init__(self: Pipeline, steps: List[Union[Step, Callable[[Context, Any], Any]]] = None, name: str = "")`__<br>
The type hints for the steps arg looks confusing. Here's what's allowed:

- Instances of the derive from `pipelayer.Filter` and implement the `run` method
- Functions (instance/class/static/module) that have the following signature `func(context: Any, data: Any)`
- Anonymous functions (lambda) with two arguments that follow the same pattern for regular functions: `my_func = lambda context, data: data`
- **Instances of [`pipelayer.Pipeline`](#pipelayer.Pipeline) (new in v0.3.0)**

***Properties***

__`manifest`__ (Manifest)<br>
An instance of [`pipelayer.Manifest`](#pipelayermanifest) that is created when the run method is called.

***Methods***

__`run(context: Union[`[`Context`](#pipelayercontext)`, Any], data: Any) -> Any`__<br>
The pipeline runner that iterates through the `steps` and pipes filter output to the next step.
<br><br>


### __`pipelayer.Filter(Step)`__
A base class with an abstract `run` method, and the optional `pre_process` and `post_process` methods.

***Properties***

__`name`__ (str)<br>
Optional. Used by the [`Manifest`](#pipelayermanifest)

__`pre_process`__ (callable)<br>
Optional.

__`post_process`__ (callable)<br>
Optional.

***Methods***

__`run(context: Union[`[`Context`](#pipelayercontext)`, Any], data: Any) -> Any`__<br>
The type of the `data` argument in the abstract class is `Any`, but you can use the correct type for the data when implementing method. The same is true for the return type.
<br><br>


### __`pipelayer.Step`__
The base class for `[pipelayer.Pipeline](#pipelayerpipeline)` and `[pipelayer.Filter](#pipelayerfilter)`.

***Properties***

__`name`__ (str)<br>
Optional. Used by the Manifest
<br><br>


### __`pipelayer.Context`__
The Context object is used to pass application-level information to each filter.

***Properties***

__[`settings`](#pipelayersettings)__ (Any)<br>
An optional abstract property for storing application-level data.

__`log`__ (Any)<br>
An optional abstract property for a common logger that can be used within pipeline filters.

__[`manifest`](#pipelayermanifest)__ (Manifest)<br>
A model that keeps a record of start/stop times for a pipeline, as well as each filter.
<br><br>


### __`pipelayer.Settings`__
The settings class is an optional base class for applications settings that inherits from `pydantic.BaseModel`.
<br><br>


### __`pipelayer.Manifest`__
The Manifest keeps a record of [`Pipeline`](#pipeline) and [`Filter`](#pipelayerfilter) activity.


### Utilities

### __`pipelayer.util.render_manifest(manifest: Manifest, indent: int = 2) -> str`__
Static function that renders formatted JSON data

