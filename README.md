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

### Step 1: Create Pipeline Filters

`hello_world_filters.py`
```python
from pipelayer import Filter


class HelloFilter(Filter):
    def run(self, data, context) -> str:
        return "Hello"


class WorldFilter(Filter):
    def run(self, data, context) -> str:
        return f"{data},  World!"
```

`functions.py`
```python
def create_message_dict(data: str, context) -> dict:
    return {"message": data}
```

### Step 2: Create a Pipeline
Create a module to run the pipeline:

`app.py`
```python
from pipelayer import Pipeline

from functions import create_message
from hello_world_filters import HelloFilter, WorldFilter


if __name__ = "__main__":
    hello_world_pipeline = Pipeline([
        HelloFilter,                           # pipeline.Filter type
        WorldFilter,                           # pipeline.Filter instance
        create_message_dict                    # function type
        lambda data, context: json.dumps(data) # anonymous function
    ])

    output = hello_world_pipeline.run()

    # output = '{"message": "Hello, World!"}'

    print(f"Pipeline Output: {output}")
    print(hello_world_pipeline.manifest.__dict__)

```

### Step 3: Run the Pipeline
from the command line:
```sh
run app.py
```

---

## The Framework
* [Pipeline](#pipelayerpipeline)
* [Filter](#pipelayerfilter)
* [Context](#pipelayercontext)
* [Manifest](#pipelayermanifest)
* [Utilities](#utilities)
<br><br>


### __`pipelayer.Pipeline(`[`Step`](#pipelayerstep)`)`__

***Constructor***

__`__init__(self: Pipeline, steps: List[Union[Step, Callable[Any, [Context]]]] = None, name: str = "")`__<br>
The type hints for the `steps` arg may look confusing. Here's what's allowed:

- Instances of the derive from `pipelayer.Filter` and implement the `run` method
- Functions (instance/class/static/module) that have the following signature `func(context: Any, data: Any)`
- Anonymous functions (lambda) with two arguments that follow the same pattern for regular functions: `my_func = lambda data, context: data`
- **Instances of [`pipelayer.Pipeline`](#pipelayer.Pipeline) (new in v0.3.0)**

***Properties***

__`manifest`__ (Manifest)<br>
An instance of [`pipelayer.Manifest`](#pipelayermanifest) that is created when the run method is called.

***Methods***

__`run(data: Any, context: Optional[`[`Context`](#pipelayercontext)`]) -> Any`__<br>
The pipeline runner that iterates through the `steps` and pipes filter output to the next step.
<br><br>


### __`pipelayer.Filter(`[`Step`](#pipelayerstep)`)`__
A base class with an abstract `run` method.

***Properties***

__`pre_process`__ (callable)<br>
Optional.

__`post_process`__ (callable)<br>
Optional.

***Methods***

__`@abstractmethod`__<br>
__`run(data: Any, context: Optional[`[`Context`](#pipelayercontext)`]) -> Any`__<br>
The abstract filter runner.
<br><br>


### __`pipelayer.Step`__
The base class that is sub-classed by [`pipelayer.Pipeline`](#pipelayerpipeline) and [`pipelayer.Filter`](#pipelayerfilter).

***Abstract Methods***

__`@abstractmethod`__<br>
__`run(data: Any, context: Optional[`[`Context`](#pipelayercontext)`]) -> Any`__<br>
The abstract

***Properties***

__`name`__ (str)<br>
Optional. Used by the Manifest
<br><br>


### __`pipelayer.Context`__
A extensible base class for runtime app config.
<br><br>


### __`pipelayer.Manifest`__
The Manifest keeps a record of [`Pipeline`](#pipeline) and [`Filter`](#pipelayerfilter) activity.


### Utilities

__`pipelayer.util.render_manifest(manifest: Manifest, indent: int = 2) -> str`__
Static function that renders formatted JSON data

