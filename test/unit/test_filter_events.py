from __future__ import annotations

import pytest
from pipelayer import Action, Filter, Pipeline
from pipelayer.event_args import EventArgs
from pipelayer.filter import raise_events


@pytest.mark.unit
class TestFilterEvents:

    @pytest.mark.happy
    def test_filter_on_start(self):

        class MyFilter(Filter):

            @raise_events
            def run(self, data, context) -> dict:
                return {"something": "goes here"}

        def myfilter_start(sender: object, args: EventArgs) -> None:
            args.action = Action.EXIT

        f = MyFilter()

        f.start.append(myfilter_start)

        p = Pipeline(steps=[f])
        response = p.run(None)

        assert response is None

    @pytest.mark.happy
    def test_filter_on_end(self):

        class MyFilter(Filter):

            @raise_events
            def run(self, data, context) -> dict:
                return {"something": "goes here"}

        def myfilter_end(sender: object, args: EventArgs) -> None:
            args.data = None
            args.action = Action.EXIT

        f = MyFilter()

        f.end.append(myfilter_end)

        p = Pipeline(steps=[f])
        response = p.run(None)

        assert response is None
