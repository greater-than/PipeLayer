import pytest


@pytest.mark.unit
class TestPublishedExamples:

    @pytest.mark.happy
    def test_getting_started(self):
        # https://greaterthan.solutions/pipelayer/
        import json

        from pipelayer import Filter, Pipeline

        class HelloFilter(Filter):
            def run(self, data, context):
                return "Hello"

        class WorldFilter(Filter):
            def run(self, data, context):
                return f"{data}, World!"

        def create_message_dict(data, context):
            return {"message": data}

        hello_world_pipeline = Pipeline([
            HelloFilter,                            # pipeline.Filter type
            WorldFilter(),                          # pipeline.Filter instance
            create_message_dict,                    # function
            lambda data, context: json.dumps(data)  # anonymous function
        ])

        output = hello_world_pipeline.run()

        assert output == '{"message": "Hello, World!"}'

    @pytest.mark.happy
    def test_v5_events(self):
        # https://greaterthan.solutions/2021/02/pipelayer-0-5-0/
        from pipelayer import Action, Filter, FilterEventArgs, Pipeline
        from pipelayer.filter import raise_events

        class MyFilter(Filter):
            @raise_events                # Raises the events
            def run(self, data, context):
                return f"{data}has been changed"

        # Handles the filter start event
        def my_filter_start(obj: Filter, args: FilterEventArgs):
            args.data = "Filter Skipped"
            args.action = Action.SKIP    # This will skip over the step

        my_filter = MyFilter()
        my_filter.start.append(my_filter_start)

        my_pipeline = Pipeline(steps=[
            my_filter
        ])

        output = my_pipeline.run("Some data...", None)
        assert output == "Filter Skipped"
        #  output is "Filter Skipped"
