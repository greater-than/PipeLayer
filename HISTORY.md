# PipeLayer: Version History

## 0.6.0
* Pipeline and Switch raise start/exit/end events
* Filter pre_process/post_process methods removed in lieu of events to simplfy pipeline runner
* Manifest models condensed


## 0.5.1
* Enables addition assigment operator for appending event handlers
* Adds `default` case for Switch filter


## 0.5.0 - 2/13/21
* Adds start/exit/filter events to `pipelayer.Filter`
* Pipeline terminates if the Filter.exit event is raised
* Adds raise_event decorator to wrap the `run` method in an implementation of `pipeline.Filter`
* consolidates create methods in `pipelayer.ManifestHelper`

## 0.4.1 - 2/9/21
* BUGFIX: fixes check for staticmethods when initializing the pipeline.

## 0.4.0 - 2/6/21
* Adds Switch filter
* Adds protocols:
  * `pipelayer.protocol.CompoundStep`
  * `pipelayer.protocol.Filter`
  * `pipelayer.protocol.Manifest`
* Moves `Step` protocol to the `piplayer.protocol` namespace
* Moves `Pipeline` into separate module
* Exposes all core classes in root `__init__.py`
* Updates LICENSE to Free BSD (previous versions still honor the MIT License)

## 0.3.1 - 2/1/21
* Adds support for classes that implement the `pipelayer.Step` protocol as steps
* `pipelayer.Step` is now a Protocol
* `pipelater.Pipeline` and `pipelayer.Filter` implement the `pipelayer.Step` protocol
* Updates type hints for pre_/post_process arguments in `pipelayer.Filter` constructor

## 0.3.0 - 1/30/21
It's still in beta and bumping the version to 1.0.0 was deferred--despite the breaking changes.

What's New:
* Nested pipelines

BREAKING CHANGES:
* `pipelayer.Pipeline.filters` attribute renamed to `steps`
* Adds support for `pipelayer.Pipeline` instances as steps
* `pipelayer.Pipeline` removes factory method, and implements a constructor that takes `steps` and `name` as args
* `pipelayer.Pipeline.run` and `pipelayer.Filter.run` method signatures updated.
* Removes `pipelayer.Settings` base class
* Removes `settings` and `log` attributes from the `pipelayer.Context` class
* Removes `pipelayer.exception.PipelineException`

## 0.2.0 - 1/22/21
* Adds support for static/module/lamba functions as well as `pipelayer.Filter` types as Pipeline Filters
* Adds Basic signature validation for filter functions
* context property in `pipelayer.Filter` is typed as `Union[Context]`
* Handles all exceptions raises by filters and raises a `PipelineException` with the original exception assigned to the `inner_exception` property

## 0.1.0 - 1/16/2021
* Pipeline composed of single-method classes that inherit from `pipelayer.Filter`
