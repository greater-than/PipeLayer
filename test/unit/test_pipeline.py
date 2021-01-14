import json

import pytest
from steampipe import Pipeline, Step


@pytest.mark.unit
class TestPipeline:

    @pytest.mark.happy
    def test_pipeline(self, app_context):
        from test.fixtures.app_context import AppContext

        def first_step_preprocess(context: AppContext, data: dict) -> dict:
            return data

        class FirstStep(Step):
            def run(self, context: AppContext, data=None) -> dict:
                return {"something": "goes here"}

        steps = [
            FirstStep(
                pre_process=first_step_preprocess,
                post_process=lambda context, data: json.dumps(data)
            )
        ]

        context = app_context
        pipeline = Pipeline.create(context)
        response = pipeline.run(steps)

        assert response == '{"something": "goes here"}'
