import pytest
from pipelayer import Pipeline
from pipelayer.event_args import PipelineEventArgs
from pipelayer.filter import Filter


class MyFilter(Filter):
    def run(self, data, context) -> dict:
        return {"something": "goes here"}


@pytest.mark.unit
class TestPipelineEvents:
    @pytest.mark.happy
    def test_pipeline_on_step_end(self, ):

        def my_filter_step_end(sender: object, args: PipelineEventArgs) -> None:
            assert args.data == {"something": "goes here"}
            assert args.manifest_entry is not None
            assert args.manifest_entry.end is not None
            assert args.manifest_entry.duration is not None

        f = MyFilter()

        p: Pipeline = Pipeline(steps=[f])
        p.step_end += my_filter_step_end

        p.run(None)

    @pytest.mark.happy
    def test_pipeline_on_step_end_2(self, ):

        def my_filter_step_end(sender: object, args: PipelineEventArgs) -> None:
            assert args.data == {"something": "goes here"}
            assert args.manifest_entry is not None
            assert args.manifest_entry.end is not None
            assert args.manifest_entry.duration is not None

        f = MyFilter()

        p: Pipeline = Pipeline(steps=[f])
        p.step_end = p.step_end + my_filter_step_end

        p.run(None)

    @pytest.mark.happy
    def test_nested_pipeline_on_step_end(self, app_context):

        def first_filter_step_end(sender: object, args: PipelineEventArgs) -> None:
            assert args.data == {"something": "goes here"}
            assert args.manifest_entry is not None
            assert args.manifest_entry.end is not None
            assert args.manifest_entry.duration is not None
            assert args.manifest_entry.steps is not None

        class FirstFilter(Filter):
            def run(self, data, context) -> dict:
                return {"something": "goes here"}

        steps = [
            FirstFilter()
        ]

        sub_pipeline = Pipeline(steps, "SubPipeline")
        pipeline = Pipeline([sub_pipeline], "OuterPipeline")
        pipeline.step_end.append(first_filter_step_end)
        response = pipeline.run(None)

        assert pipeline.name == "OuterPipeline"
        assert pipeline.manifest.name == "OuterPipeline"
        assert pipeline.manifest.steps[0].name == "SubPipeline"
        assert response == {"something": "goes here"}
        assert isinstance(pipeline.manifest.__dict__, dict)

    @pytest.mark.sad
    def test_assigning_wrong_type_to_step_end_handler(self):
        f = MyFilter()

        p: Pipeline = Pipeline(steps=[f])

        with pytest.raises(TypeError):
            p.step_end = []
