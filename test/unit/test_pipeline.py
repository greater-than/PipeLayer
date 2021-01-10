import json
from logging import Logger

import pytest
from steampipe.context import Context
from steampipe.pipeline import Pipeline
from steampipe.step import Step


@pytest.mark.unit
class TestPipeline:
    def test_pipeline(self):

        def first_step_preprocess(data: dict) -> dict:
            return data

        class FirstStep(Step):
            def execute(self, context: Context) -> dict:
                return {"something": "goes here"}

        steps = [
            FirstStep(pre_process=first_step_preprocess, post_process=json.dumps)
        ]

        context = Context(settings=None, log=Logger("Pipeline Logger"))
        context.data = {}

        response = Pipeline(context).run(steps)

        assert response
