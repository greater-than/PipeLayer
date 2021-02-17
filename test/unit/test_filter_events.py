from __future__ import annotations

import pytest
from pipelayer import Action, Context, Filter, FilterEventArgs, Pipeline
from pipelayer.filter import _parse_args, raise_events


class MyFilter(Filter):
    @raise_events
    def run(self, data, context) -> dict:
        return {"something": "goes here"}


@pytest.mark.unit
class TestFilterEvents:

    @pytest.mark.happy
    def test_filter_on_start(self):

        def myfilter_start(sender: object, args: FilterEventArgs) -> None:
            args.action = Action.EXIT

        f = MyFilter()

        f.start += myfilter_start

        p = Pipeline(steps=[f])
        response = p.run(None)

        assert response is None

    @pytest.mark.happy
    def test_filter_on_end(self):

        def myfilter_end(sender: object, args: FilterEventArgs) -> None:
            args.data = None
            args.action = Action.EXIT

        f = MyFilter()

        f.end.append(myfilter_end)

        p = Pipeline(steps=[f])
        response = p.run(None)

        assert response is None

    @pytest.mark.happy
    def test_event_handler_assignment(self):

        def my_event_handler(sender: Filter, args: FilterEventArgs):
            pass

        my_filter = MyFilter()
        my_filter.start += my_event_handler
        my_filter.start.append(my_event_handler)
        my_filter.start = my_filter.start + my_event_handler

        my_filter.exit += my_event_handler
        my_filter.exit.append(my_event_handler)
        my_filter.exit = my_filter.start + my_event_handler

        my_filter.end += my_event_handler
        my_filter.end.append(my_event_handler)
        my_filter.end = my_filter.start + my_event_handler

        assert True

    @pytest.mark.sad
    def test_assigning_wrong_type_to_handlers(self):
        class MyFilter(Filter):
            def run(self, data, context) -> dict:
                pass

        with pytest.raises(TypeError):
            MyFilter().start = []

        with pytest.raises(TypeError):
            MyFilter().exit = []

        with pytest.raises(TypeError):
            MyFilter().end = []

    @pytest.mark.happy
    def test_parse_args_2_args(self):

        class MyFilter(Filter):
            def run(self, data) -> dict:
                pass

        my_filter = MyFilter()
        a, b, c = _parse_args(my_filter, "xyz")

        assert a is my_filter
        assert b == "xyz"
        assert isinstance(c, Context)

    @pytest.mark.happy
    def test_parse_kwargs(self):

        class MyFilter(Filter):
            def run(self, data) -> dict:
                pass

        my_filter = MyFilter()
        a, b, c = _parse_args(my_filter, data="xyz")

        assert a is my_filter
        assert b == "xyz"
        assert isinstance(c, Context)
