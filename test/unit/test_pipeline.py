import json

import pytest
from pipelayer import Filter, Pipeline


@pytest.mark.unit
class TestPipeline:

    @pytest.mark.happy
    def test_pipeline_basic(self, app_context):
        from test.fixtures.app_context import AppContext

        def first_filter_preprocess(context: AppContext, data: dict) -> dict:
            return data

        class FirstFilter(Filter):
            def run(self, context: AppContext, data=None) -> dict:
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
        from test.fixtures.app_context import AppContext

        class FirstFilter(Filter):
            def run(self, context: AppContext, data=None) -> dict:
                return {"something": "goes here"}

        def second_filter(context: AppContext, data: dict) -> dict:
            data.update({"something": "got changed"})
            return data

        filters = [
            FirstFilter,
            second_filter
        ]

        context = app_context
        pipeline = Pipeline.create(context)
        response = pipeline.run(filters)

        assert pipeline.name == "Pipeline"
        assert pipeline.manifest.name == "Pipeline"
        assert pipeline.manifest.filters[0].name == ""
        assert response == {"something": "got changed"}
        assert isinstance(pipeline.manifest.__dict__, dict)
