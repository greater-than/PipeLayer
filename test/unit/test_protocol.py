import pytest


@pytest.mark.unit
class TestProtocol:

    @pytest.mark.sad
    def test_step(self):
        from pipelayer.step import Step
        with pytest.raises(NotImplementedError):
            Step.run(None, None, None)

    @pytest.mark.sad
    def test_pipeline(self):
        from pipelayer.pipeline import Pipeline
        with pytest.raises(NotImplementedError):
            Pipeline.run_steps(None, None, None)
