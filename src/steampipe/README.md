# SteamPipe
Steampipe is a light-weight pipeline framework. Define a series of steps, and chain them together to create plug-and-play applications.

## Table of Contents
* [Getting Started](#getting-started)
    * [Installation](#installation)
* [The Pipeline](#the-pipeline)
* [The Pipeline Context](#the-pipeline-context)
* [Steps](steps)

## Getting Started

### Installation

From the command line:
```sh
pip install steampipe
```

### The Pipeline

To create a pipeline:

```
from steampipe import Context, Pipeline

my_context = Context

my_pipeline = Pipeline()
```

### The Pipeline Context
A Context object is used to pass application-level information to each step. The Context class contains two properties `settings` and `log`.

* `settings` is where you can store key-value pairs that the application uses.
* `log` is a logger, by default it uses the built-in Python Logger

### Steps
Create a class that inherits from `steampipe.Step` abstract class, and implements the execute method.

```
from steampipe import Context, Step


class MyStep(Step):
    def execute(context: Context, data: Any) -> Any:
        ...
```

The type of the `data` argument in the abstract class is `Any`, but you can use the correct type for the data in this method. The same is true for the return type.