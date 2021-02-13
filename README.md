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
* [Switch](#switch)
* [Filter](#filter)
  * [Events](#filterevents)
  * [FilterEventArgs](#eventargs)
* [Context](#context)
* [Manifest](#manifest)
* [Utilities](#utilities)
<br><br>


<div id="pipeline"></div>

### __`pipelayer.Pipeline`__
__`__init__(steps, name)`__

*args:*

- `steps: List[Union[Step, Callable[[Any, Context], Any]]]`<br>
A list of:
  - Classes and Instances that derive from `pipelayer.Filter` and implement the `run` method
  - Classes that implement the `pipelayer.Step` protocol
  - Functions (instance/class/static/module) that have the following signature

    ```python
    def func(data: Any, context: Any)
    ```

  - Anonymous functions (lambda) with two arguments that follow this pattern:

    ```python
    my_func = lambda data, context: data
    ```

  - Instances of `pipelayer.Pipeline`

- `name: Optional[str]`<br>
   If not specified, the class name will be used.

***Properties:***

__`name: str`__<br>

__`state: Pipeline.State`__<br>

__`steps: List[Union[Step, Callable[[Any, Context], Any]]]`__<br>

__`manifest: Manifest`__<br>
An instance of [`pipelayer.Manifest`](#manifest) that is created when the run method is called.

***Methods:***

__`run(data, context) -> Any`__<br>
The pipeline runner that iterates through the `steps` and pipes filter output to the next step.

*args:*

- `data: Any`
- `context: pipelayer.Context`
<br><br>


<div id="switch"></div>

### __`pipelayer.Switch`__
___`__init__(expression, cases, name)`___<br>
An implementation of a Switch statement as a pipeline filter

*args:*
- `expression: Union[Step, Callable[[Any, Context], Any]]`
- `cases: Dict[Union[Step, Callable[[Any, Context], Any]]]`
- `name: Optional[str]`<br>
   If not specified, the class name will be used.


***Properties:***

__`expression: Union[Step, Callable[[Any, Context], Any]]`__<br>
__`cases: Dict[Union[Step, Callable[[Any, Context], Any]]]`__<br>
__`name: Optional[str]`__<br>
__`manifest: Manifest`__

***Methods:***

__`run(data, context) -> Any`__<br>
The switch runner that evaluates the specified expresssion executes the matching case.
<br><br>


<div id="filter"></div>

### __`pipelayer.Filter`__
___`__init__(name, pre_process, post_process)`___

*args:*
- `name: Optional[str]`<br>
   If not specified, the class name will be used.
- `pre_process: Optional[Callable[[Any, Context], Any]`
- `post_process: Optional[Callable[[Any, Context], Any]`


***Properties:***

__`pre_process: Optional[Callable[[Any, Context], Any]`__<br>
__`post_process: Optional[Callable[[Any, Context], Any]`__<br>

<div id="filterevents"></div>

***Events:***<br>
Events are lists of callables assignable after instantiation and are raised if the `pipelayer.filter.raise_events` decorator is applied to the implementation of the `run` method.

__`start: List[Callable[[Filter, Any], Any]]`__<br>
Raised before the `run` method is invoked.

__`exit: List[Callable[[Filter, Any], Any]]`__<br>
Raised if `action` is set to `Action.SKIP` or `Action.EXIT` in either a `start` or `stop` event handler.

__`end: List[Callable[[Filter, Any], Any]]`__<br>
Raised after the `run` method is invoked.
<br><br>


<div id="eventargs"></div>

### __`pipelayer.FilterEventArgs`__
___`__init__(data, context, state)`___

*args:*
- `data: Any`<br>
- `context: Context`
- `state: State`<br><br>

<div id="context"></div>

### __`pipelayer.Context`__
A abstract base class for runtime app data.
<br><br>


<div id="manifest"></div>

### __`pipelayer.Manifest`__
The Manifest keeps a record of [`Pipeline`](#pipeline) and [`Filter`](#filter) activity.


### Utilities

__`pipelayer.util.render_manifest(manifest, indent) -> str`__<br>
Static function that renders formatted JSON data

*args:*

- `manifest: Manifest`
- `indent: Optional[int]`<br>
  Default value is 2.

