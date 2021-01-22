import json

import pytest
from pipelayer import Filter, Pipeline
from pipelayer.exception import InvalidFilterException, PipelineException
from pipelayer.util import MockFilter


@pytest.mark.unit
class TestPipeline:

    @pytest.mark.happy
    def test_pipeline_basic(self, app_context):

        def first_filter_preprocess(context, data) -> dict:
            return data

        class FirstFilter(Filter):
            def run(self, context, data) -> dict:
                return {"something": "goes here"}

        filters = [
            FirstFilter(
                pre_process=first_filter_preprocess,
                post_process=lambda context, data: json.dumps(data)
            )
        ]

        context = app_context
        pipeline = Pipeline.create(context)
        response = pipeline.run(filters)

        assert pipeline.name == "Pipeline"
        assert pipeline.manifest.name == "Pipeline"
        assert pipeline.manifest.filters[0].name == "FirstFilter"
        assert response == '{"something": "goes here"}'
        assert isinstance(pipeline.manifest.__dict__, dict)

    @pytest.mark.happy
    def test_pipeline_static_filter_funcs(self, app_context):
        import json

        class FirstFilter(Filter):
            def run(self, context, data) -> dict:
                return {"something": "goes here"}

        def second_filter(context, data) -> dict:
            data.update({"something": "got changed"})
            return data

        filters = [
            FirstFilter,
            second_filter,
            lambda context, data: json.dumps(data)
        ]

        context = app_context
        pipeline = Pipeline.create(context)
        response = pipeline.run(filters)

        assert pipeline.name == "Pipeline"
        assert pipeline.manifest.name == "Pipeline"
        assert pipeline.manifest.filters[0].name == "FirstFilter"
        assert pipeline.manifest.filters[1].name == "second_filter"
        assert pipeline.manifest.filters[2].name == "[lambda context, data: json.dumps(data)]"
        assert response == '{"something": "got changed"}'
        assert isinstance(pipeline.manifest.__dict__, dict)

    @pytest.mark.sad
    def test_initialize_filter_invalid_filter(self):
        with pytest.raises(InvalidFilterException):
            Pipeline._Pipeline__initialize_filter(None)

    @pytest.mark.sad
    def test_filter_raises_exception(self):

        class ExceptionFilter(Filter):
            def run(self, context, data) -> dict:
                raise FileNotFoundError("This is not the file you're looing for.")

        filters = [ExceptionFilter]
        pipeline = Pipeline.create(None, None)

        with pytest.raises(PipelineException):
            pipeline.run(filters, None)

    @pytest.mark.sad
    def test_pre_process_raises_exception(self):

        def none_type_func(context, data):
            raise TypeError("You're not my type.")

        filters = [MockFilter(pre_process=none_type_func)]
        pipeline = Pipeline.create(None, None)

        with pytest.raises(PipelineException):
            pipeline.run(filters, None)

    @pytest.mark.sad
    def test_post_process_raises_exception(self):
        from pipelayer.util import MockFilter

        def none_type_func(context, data):
            raise TypeError("You're not my type either.")

        filters = [MockFilter(post_process=none_type_func)]
        pipeline = Pipeline.create(None, None)

        with pytest.raises(PipelineException):
            pipeline.run(filters, None)
