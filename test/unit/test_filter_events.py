from __future__ import annotations

import pytest
from pipelayer import Action, Filter, FilterEventArgs, Pipeline
from pipelayer.filter import raise_events


@pytest.mark.unit
class TestFilterEvents:

    @pytest.mark.happy
    def test_filter_on_start(self):

        class MyFilter(Filter):

            @raise_events
            def run(self, data, context) -> dict:
                return {"something": "goes here"}

        def myfilter_start(sender: object, args: FilterEventArgs) -> None:
            args.action = Action.EXIT

        f = MyFilter()

        f.start += myfilter_start

        p = Pipeline(steps=[f])
        response = p.run(None)

        assert response is None

    @pytest.mark.happy
    def test_filter_on_end(self):

        class MyFilter(Filter):

            @raise_events
            def run(self, data, context) -> dict:
                return {"something": "goes here"}

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
        class MyFilter(Filter):
            def run(self, data, context) -> dict:
                ...

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
