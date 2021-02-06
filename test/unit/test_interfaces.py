import pytest


@pytest.mark.unit
class TestInterfaces:

    @pytest.mark.sad
    def test_step(self):
        from pipelayer.step.protocol import Step

        with pytest.raises(NotImplementedError):
            Step.run(None, None, None)

    @pytest.mark.sad
    def test_compound_step(self):
        from pipelayer.compound_step.protocol import CompoundStep

        with pytest.raises(NotImplementedError):
            CompoundStep._run_steps(None, None, None)

        with pytest.raises(NotImplementedError):
            CompoundStep.run(None, None, None)
