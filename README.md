# PipeLayer
PipeLayer is a lightweight Python pipeline framework. Define a series of steps, and chain them together to create modular applications.
<br>

### Table of Contents

* [Installation](#install)
* [Getting Started](#get-started)
* [The Framework](http://greaterthan.solutions/pipelayer/framework)<br>
  Documentation has been moved to [greaterthan.solutions](http://greaterthan.solutions/pipelayer)
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
