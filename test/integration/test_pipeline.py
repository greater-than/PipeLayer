import json

import pytest
from pipelayer import Filter, Pipeline


@pytest.mark.integration
class TestPipeline:

    @pytest.mark.happy
    def test_simple_pipeline(self, app_context):
        from test.fixtures.app_context import AppContext

        def first_filter_preprocess(context: AppContext, data: dict) -> dict:
            return data

        class FirstFilter(Filter):
            def run(self, context: AppContext, data=None) -> dict:
                return {"something": "goes here"}

        filters = [
            FirstFilter(
                pre_process=first_filter_preprocess,
                post_process=lambda c, d: json.dumps(d)
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
