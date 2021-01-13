import json

import pytest
from steampipe.pipeline import Pipeline
from steampipe.step import Step


@pytest.mark.integration
class TestPipeline:

    @pytest.mark.happy
    def test_simple_pipeline(self, app_context):
        from test.fixtures.app_context import AppContext

        def first_step_preprocess(context: AppContext, data: dict) -> dict:
            return data

        class FirstStep(Step):
            def execute(self, context: AppContext, data=None) -> dict:
                return {"something": "goes here"}

        steps = [
            FirstStep(
                pre_process=first_step_preprocess,
                post_process=lambda c, d: json.dumps(d)
            )
        ]

        context = app_context
        pipeline = Pipeline.create(context)
        response = pipeline.run(steps)

        assert pipeline.name == "Pipeline"
        assert pipeline.manifest.name == "Pipeline"
        assert pipeline.manifest.steps[0].name == "FirstStep"
        assert response == '{"something": "goes here"}'
        assert isinstance(pipeline.manifest.__dict__, dict)
