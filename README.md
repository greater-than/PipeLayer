# PipeLayer

[![LATEST](https://img.shields.io/github/v/release/greater-than/pipelayer?style=for-the-badge&logo=PyPi&logoColor=white)](https://pypi.org/project/pipelayer/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pipelayer?style=for-the-badge&logo=Python&logoColor=white)
[![PyPI - License](https://img.shields.io/pypi/l/pipelayer?style=for-the-badge)](LICENSE)


PipeLayer is a event-driven pipeline framework. Define a series of steps, and chain them together to create modular applications.
<br>

### Table of Contents

* [Installation](#install)
* [Getting Started](#get-started)
* [The Framework](http://greaterthan.solutions/pipelayer/framework)<br>
  *Complete documentation can be found here: [greaterthan.solutions/pipelayer](http://greaterthan.solutions/pipelayer)*
<br><br>


<div id="install"></div>

## Installation

From the command line:
```sh
pip install pipelayer
```


<div id="get-started"></div>

## Getting Started

### Step 1: Create The Filters

`hello_world_filters.py`
```python
from pipelayer import Filter


class HelloFilter(Filter):
    def run(self, data, context):
        return "Hello"


class WorldFilter(Filter):
    def run(self, data, context):
        return f"{data}, World!"
```

`functions.py`
```python
def create_message(data, context):
    return {"message": data}
```

### Step 2: Create The Pipeline
Create a module to run the pipeline:

`app.py`
```python
import json
from pipelayer import Pipeline
from pipelayer.util import render_manifest

from functions import create_message
from hello_world_filters import HelloFilter, WorldFilter


if __name__ == "__main__":
    hello_world_pipeline = Pipeline(
        [
            HelloFilter,
            WorldFilter,
            create_message,
            lambda data, context: json.dumps(data),
        ]
    )

    output = hello_world_pipeline.run(None)

    # output = '{"message": "Hello, World!"}'

    print("\nPipeline Output:")
    print(output)
    print("\nManifest:")
    print(render_manifest(hello_world_pipeline.manifest))

```

### Step 3: Run the Pipeline
from the command line:
```sh
run app.py
```
