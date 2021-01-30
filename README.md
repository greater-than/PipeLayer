# PipeLayer
PipeLayer is a lightweight Python pipeline framework. Define a series of steps, and chain them together to create modular applications.
<br>

### Table of Contents

* [Installation](#install)
* [Getting Started](#get-started)
* [The Framework](#framework)
<br><br>


<div id="install"></div>

## Installation

From the command line:
```sh
pip install pipelayer
```


<div id="get-started"></div>

## Getting Started

### Step 1: Create Pipeline Filters

`hello_world_filters.py`
```python
from pipelayer import Filter


class HelloFilter(Filter):
    def run(self, data, context):
        return "Hello"


class WorldFilter(Filter):
    def run(self, data, context):
        return f"{data},  World!"
```

`functions.py`
```python
def create_message_dict(data, context):
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

<div id="framework"></div>

## The Framework
* [Pipeline](#pipeline)
* [Filter](#filter)
* [Context](#context)
* [Manifest](#manifest)
* [Utilities](#utilities)
<br><br>


<div id="pipeline"></div>

### __`pipelayer.Pipeline(`[`Step`](#step)`)`__

***Constructor***

__`__init__(self: Pipeline, steps: List[Union[Step, Callable[Any, [Context]]]] = None, name: str = "")`__<br>
The type hints for the `steps` arg may look confusing. Here's what's allowed:

- Classes and Instances that derive from `pipelayer.Filter` and implement the `run` method
- Functions (instance/class/static/module) that have the following signature

  ```python
  def func(data: Any, context: Any)
  ```

- Anonymous functions (lambda) with two arguments that follow the same pattern for regular functions:

  ```python
  my_func = lambda data, context: data
  ```

- **Instances of `pipelayer.Pipeline` (new in v0.3.0)**

***Properties***

__`manifest`__ (Manifest)<br>
An instance of [`pipelayer.Manifest`](#manifest) that is created when the run method is called.

***Methods***

__`run(data: Any, context: Optional[`[`Context`](#context)`]) -> Any`__<br>
The pipeline runner that iterates through the `steps` and pipes filter output to the next step.
<br><br>


<div id="filter"></div>

### __`pipelayer.Filter(`[`Step`](#step)`)`__
A base class with an abstract `run` method.

***Properties***

__`pre_process`__ (callable)<br>
Optional.

__`post_process`__ (callable)<br>
Optional.

***Methods***

__`@abstractmethod`__<br>
__`run(data: Any, context: Optional[`[`Context`](#context)`]) -> Any`__<br>
The abstract filter runner.
<br><br>


<div id="step"></div>

### __`pipelayer.Step`__
The base class that is sub-classed by [`pipelayer.Pipeline`](#pipeline) and [`pipelayer.Filter`](#filter).

***Abstract Methods***

__`@abstractmethod`__<br>
__`run(data: Any, context: Optional[`[`Context`](#context)`]) -> Any`__<br>
The abstract

***Properties***

__`name`__ (str)<br>
Optional. Used by the Manifest
<br><br>


<div id="context"></div>

### __`pipelayer.Context`__
A extensible base class for runtime app config.
<br><br>


<div id="manifest"></div>

### __`pipelayer.Manifest`__
The Manifest keeps a record of [`Pipeline`](#pipeline) and [`Filter`](#filter) activity.


### Utilities

__`pipelayer.util.render_manifest(manifest: Manifest, indent: int = 2) -> str`__<br>
Static function that renders formatted JSON data

