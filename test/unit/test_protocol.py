import pytest


@pytest.mark.unit
class TestProtocol:

    @pytest.mark.sad
    def test_step(self):
        from pipelayer.step import Step
        with pytest.raises(NotImplementedError):
            Step.run(None, None, None)

    @pytest.mark.sad
    def test_compound_step(self):
        from pipelayer.compound_step import CompoundStep
        with pytest.raises(NotImplementedError):
            CompoundStep.run_steps(None, None, None)
