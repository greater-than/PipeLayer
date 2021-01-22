# Version History

## 0.2.0 - 1/23/21
* Adds support for static/module/lamba methods as well as `pipelayer.Filter` types as Pipeline Filters
* Adds support for type of `pipelayer.Filter` as Pipeline Filters
* Basic signature validation for filter functions
* context property in `pipelayer.Filter` is typed as `Union[Context, Any]`
* Handles all exceptions raises by filters and raises a `PipelineException` with the original exception assigned to the `inner_exception` property

## 0.1.0 - 1/16/2021
* Pipeline composed of single-method classes that inherit from `pipelayer.Filter`
