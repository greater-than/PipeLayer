# Version History

## 0.3.0 - 1/30/21
It's still in beta and bumping the version to 1.0.0 was deferred--despite the breaking changes.

What's New:
* Nested pipelines

BREAKING CHANGES:
* `pipelayer.Pipeline.filters` attribute renamed to `steps`
* Adds support for `pipelayer.Pipeline` instances as steps
* `pipelayer.Pipeline` removes factory method, and implements a constructor that takes `steps` and `name` as args
* `pipelayer.Pipeline.run` and `pipelayer.Filter.run` method signatures updated.
* Removed `pipelayer.Settings` base class
* Removed `settings` and `log` attributes from the `pipelayer.Context` class
* Removed `pipelayer.exception.PipelineException`

## 0.2.0 - 1/22/21
* Adds support for static/module/lamba functions as well as `pipelayer.Filter` types as Pipeline Filters
* Basic signature validation for filter functions
* context property in `pipelayer.Filter` is typed as `Union[Context]`
* Handles all exceptions raises by filters and raises a `PipelineException` with the original exception assigned to the `inner_exception` property

## 0.1.0 - 1/16/2021
* Pipeline composed of single-method classes that inherit from `pipelayer.Filter`
