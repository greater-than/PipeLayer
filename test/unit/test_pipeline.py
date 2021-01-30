import json

import pytest
from pipelayer import Filter, Pipeline
from pipelayer.exception import InvalidFilterException
from pipelayer.util import MockFilter


@pytest.mark.unit
class TestPipeline:

    @pytest.mark.happy
    def test_pipeline_basic(self, app_context):

        def first_filter_preprocess(data, context) -> dict:
            return data

        class FirstFilter(Filter):
            def run(self, data, context) -> dict:
                return {"something": "goes here"}

        steps = [
            FirstFilter(
                pre_process=first_filter_preprocess,
                post_process=lambda data, context: json.dumps(data)
            )
        ]

        pipeline = Pipeline(steps)
        response = pipeline.run(None)

        assert pipeline.name == "Pipeline"
        assert pipeline.manifest.name == "Pipeline"
        assert pipeline.manifest.steps[0].name == "FirstFilter"
        assert response == '{"something": "goes here"}'
        assert isinstance(pipeline.manifest.__dict__, dict)

    @pytest.mark.happy
    def test_nested_pipeline(self, app_context):

        def first_filter_preprocess(data, context) -> dict:
            return data

        class FirstFilter(Filter):
            def run(self, data, context) -> dict:
                return {"something": "goes here"}

        steps = [
            FirstFilter(
                pre_process=first_filter_preprocess,
                post_process=lambda data, context: json.dumps(data)
            )
        ]

        sub_pipeline = Pipeline(steps, "SubPipeline")
        pipeline = Pipeline([sub_pipeline], "OuterPipeline")
        response = pipeline.run(None)

        assert pipeline.name == "OuterPipeline"
        assert pipeline.manifest.name == "OuterPipeline"
        assert pipeline.manifest.steps[0].name == "SubPipeline"
        assert response == '{"something": "goes here"}'
        assert isinstance(pipeline.manifest.__dict__, dict)

    @pytest.mark.happy
    def test_pipeline_static_filter_funcs(self, app_context):
        import json

        class FirstFilter(Filter):
            def run(self, data, context) -> dict:
                return {"something": "goes here"}

        def second_filter(data, context) -> dict:
            data.update({"something": "got changed"})
            return data

        steps = [
            FirstFilter,
            second_filter,
            lambda data, context: json.dumps(data)
        ]

        pipeline = Pipeline(steps)
        response = pipeline.run(None)

        assert pipeline.name == "Pipeline"
        assert pipeline.manifest.name == "Pipeline"
        assert pipeline.manifest.steps[0].name == "FirstFilter"
        assert pipeline.manifest.steps[1].name == "second_filter"
        assert pipeline.manifest.steps[2].name == "<lambda data, context: json.dumps(data)>"
        assert response == '{"something": "got changed"}'
        assert isinstance(pipeline.manifest.__dict__, dict)

    @pytest.mark.sad
    def test_initialize_filter_invalid_filter(self):
        with pytest.raises(InvalidFilterException):
            Pipeline._Pipeline__initialize_step(None)

    @pytest.mark.sad
    def test_filter_raises_exception(self):

        class ExceptionFilter(Filter):
            def run(self, data, context) -> dict:
                raise FileNotFoundError("This is not the file you're looing for.")

        steps = [ExceptionFilter]
        pipeline = Pipeline(steps)

        with pytest.raises(FileNotFoundError):
            pipeline.run(None)

    @pytest.mark.sad
    def test_pre_process_raises_exception(self):

        def none_type_func(data, context):
            raise TypeError("You're not my type.")

        steps = [MockFilter(pre_process=none_type_func)]
        pipeline = Pipeline(None)

        pipeline = Pipeline(steps)

        with pytest.raises(TypeError):
            pipeline.run(None)

    @pytest.mark.sad
    def test_post_process_raises_exception(self):
        from pipelayer.util import MockFilter

        def none_type_func(data, context):
            raise TypeError("You're not my type either.")

        pipeline = Pipeline([MockFilter(post_process=none_type_func)])

        with pytest.raises(TypeError):
            pipeline.run(None)
