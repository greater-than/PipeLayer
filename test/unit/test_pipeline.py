import json

import pytest
from pipelayer import Filter, Pipeline
from pipelayer.filter import raise_events


@pytest.mark.unit
class TestPipeline:

    @pytest.mark.happy
    def test_pipeline_interface_implemented(self):
        from pipelayer.protocol import ICompoundStep
        assert isinstance(Pipeline([]), ICompoundStep)

    @pytest.mark.happy
    def test_pipeline_basic(self, app_context):

        def first_filter_preprocess(data, context) -> dict:
            return data

        class FirstFilter(Filter):
            @raise_events
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
        m = pipeline.manifest

        assert pipeline.name == "Pipeline"
        assert pipeline.manifest.name == "Pipeline"
        assert pipeline.manifest.steps[0].name == "FirstFilter"
        assert response == '{"something": "goes here"}'
        assert isinstance(m.__dict__, dict)

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
    def test_pipeline_all_filter_types(self, app_context):

        class FirstFilter(Filter):
            def run(self, data, context) -> dict:
                return {"message": "The cat in that box is dead"}

        def second_filter(data, context) -> dict:
            data["message"] += ", or maybe not."
            return data

        class ThirdFilter:
            def __init__(self, name: str) -> None:
                self.name = name

            def run(self, data, context) -> dict:
                data["message"] += " We'll never know."
                return data

        class FourthFilter:
            @staticmethod
            def get_attribution(data, context) -> dict:
                data["message"] += " --Schrodinger"
                return data

        class FifthFilter:
            @staticmethod
            def run(data, context) -> dict:
                return data

        class SixthFilter(Filter):
            @staticmethod
            def run(data, context) -> dict:
                return data

        pipeline = Pipeline([
            FifthFilter,
            SixthFilter
        ])

        steps = [
            pipeline,
            FirstFilter,
            second_filter,
            ThirdFilter("'We\'ll never know' Filter"),
            FourthFilter.get_attribution,
            FifthFilter,
            SixthFilter(),
            lambda data, context: json.dumps(data)
        ]

        pipeline = Pipeline(steps, "Schrodinger's Pipeline")
        response = pipeline.run(None)

        assert pipeline.name == "Schrodinger's Pipeline"
        assert pipeline.manifest.name == "Schrodinger's Pipeline"
        assert pipeline.manifest.steps[0].name == "Pipeline"
        assert pipeline.manifest.steps[1].name == "FirstFilter"
        assert pipeline.manifest.steps[2].name == "second_filter"
        assert pipeline.manifest.steps[3].name == "'We\'ll never know' Filter"
        assert pipeline.manifest.steps[4].name == "get_attribution"
        assert pipeline.manifest.steps[5].name == "FifthFilter"
        assert pipeline.manifest.steps[6].name == "SixthFilter"
        assert pipeline.manifest.steps[7].name == "<lambda data, context: json.dumps(data)>"
        assert response == '{"message": "The cat in that box is dead, or maybe not. We\'ll never know. --Schrodinger"}'
        assert isinstance(pipeline.manifest.__dict__, dict)

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

        class MockFilter(Filter):
            def run(self, data, context):
                return data
        steps = [MockFilter(pre_process=none_type_func)]
        pipeline = Pipeline(None)

        pipeline = Pipeline(steps)

        with pytest.raises(TypeError):
            pipeline.run(None)

    @pytest.mark.sad
    def test_post_process_raises_exception(self):
        def none_type_func(data, context):
            raise TypeError("You're not my type either.")

        class MockFilter(Filter):
            def run(self, data, context):
                return data

        pipeline = Pipeline([MockFilter(post_process=none_type_func)])

        with pytest.raises(TypeError):
            pipeline.run(None)
