from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Tuple, cast

from pipelayer.context import Context
from pipelayer.enum import Action, State
from pipelayer.event_args import FilterEventArgs, PipelineEventArgs
from pipelayer.manifest import Manifest
from pipelayer.protocol import IFilter, IPipeline

# region Pipeline


def _parse_pipeline_event_args(*args: str, **kwargs: dict) -> Tuple[IPipeline, Any, Manifest]:

    if len(args) == 3:
        return cast(IPipeline, args[0]), args[1], cast(Manifest, args[3])

    _self = None
    _data = None
    _manifest_entry = None
    _args: list = list(args)

    if _args and isinstance(args[0], IPipeline):
        _self = cast(IPipeline, _args[0])
        _args.pop(0)

    if _args:
        _data = _args[0]
        _args.pop(0)

    if kwargs:
        _data = _data or kwargs.get("data")
        _manifest_entry = _data or kwargs.get("manifest_entry")

    return cast(IPipeline, _self), _data, cast(Manifest, _manifest_entry)


def raise_pipeline_events(func: Callable) -> Callable:
    """
    Decorates a filter method to raise events
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        pipeline: IPipeline
        data: Any
        manifest_entry: Manifest
        pipeline, data, manifest_entry = _parse_pipeline_event_args(*args, **kwargs)

        evt_args: PipelineEventArgs = PipelineEventArgs(data, manifest_entry)

        pipeline._on_step_start(evt_args)

        data = func(*args, **kwargs)

        evt_args = PipelineEventArgs(data, manifest_entry)
        pipeline._on_step_end(evt_args)

        return data
    return wrapper

# endregion


# region Filter

def _parse_filter_event_args(*args: str, **kwargs: dict) -> Tuple[IFilter, Any, Context]:

    if len(args) == 3:
        return cast(IFilter, args[0]), args[1], cast(Context, args[2])

    _self = None
    _data = None
    _context = None
    _args: list = list(args)

    if _args and isinstance(args[0], IFilter):
        _self = cast(IFilter, _args[0])
        _args.pop(0)

    if _args:
        _data = _args[0]
        _args.pop(0)

    if kwargs:
        _data = _data or kwargs.get("data")
        _context = _context or kwargs.get("context")

    return cast(IFilter, _self), _data, cast(Context, _context) if _context else Context()


def raise_filter_events(func: Callable) -> Callable:
    """
    Decorates a filter method to raise events
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        filter, data, context = _parse_filter_event_args(*args, **kwargs)

        evt_args = FilterEventArgs(data, context, State.RUNNING)

        filter._on_start(evt_args)

        if evt_args.action in (Action.EXIT, Action.SKIP):
            evt_args.state = State.SKIPPING if evt_args.action == Action.SKIP else State.EXITING
            filter._on_exit(evt_args)
            return evt_args.data

        data = func(*args, **kwargs)

        evt_args = FilterEventArgs(data, context, State.COMPLETING)
        filter._on_end(evt_args)

        if evt_args.action is Action.EXIT:
            evt_args.state = State.EXITING
            filter._on_exit(evt_args)
            return evt_args.data

        return data
    return wrapper

# endregion
