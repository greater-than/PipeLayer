import pytest
from pipelayer import Filter, Pipeline
from pipelayer.enum import Action
from pipelayer.event_args import FilterEventArgs
from pipelayer.filter import raise_events


@pytest.mark.unit
class TestPipelineEventBubbling:

    @pytest.mark.happy
    def test_bubbles(self):

        class FirstFilter(Filter):
            @raise_events
            def run(self, data, context) -> dict:
                return {"message": "First filter run."}

        class SecondFilter(Filter):
            @raise_events
            def run(self, data, context) -> dict:
                return {"message": "Second filter run"}

        def first_filter_start(sender: Filter, args: FilterEventArgs) -> None:
            args.data = "EXITED!"
            args.action = Action.EXIT

        def second_filter_start(sender: Filter, args: FilterEventArgs) -> None:
            args.action = Action.CONTINUE

        first_filter = FirstFilter()
        first_filter.start += first_filter_start

        second_filter = SecondFilter()
        second_filter.start += second_filter_start

        bubbly_pipeline = Pipeline(
            name="Outer Pipeline",
            steps=[
                Pipeline(
                    name="Middle Pipeline",
                    steps=[
                        Pipeline(
                            name="Inner Pipeline",
                            steps=[
                                first_filter,
                                second_filter
                            ]
                        )

                    ]
                )
            ]
        )
        response = bubbly_pipeline.run(None)

        assert bubbly_pipeline.name == "Outer Pipeline"
        assert bubbly_pipeline.manifest.name == "Outer Pipeline"
        assert response == "EXITED!"
        assert isinstance(bubbly_pipeline.manifest.__dict__, dict)
