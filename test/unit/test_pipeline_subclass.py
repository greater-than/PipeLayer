import pytest


@pytest.mark.unit
class TestPipelineSubClass:

    @pytest.mark.sad
    def test_subclass_pipeline(self):
        from pipelayer import Pipeline
        with pytest.raises(TypeError):
            class MyPipeline(Pipeline):
                pass
