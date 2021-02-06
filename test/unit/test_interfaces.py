import pytest


@pytest.mark.unit
class TestInterfaces:

    @pytest.mark.sad
    def test_step(self):
        from pipelayer.protocol.step import Step

        with pytest.raises(NotImplementedError):
            Step.run(None, None, None)

    @pytest.mark.sad
    def test_compound_step(self):
        from pipelayer.protocol.compound_step import CompoundStep

        with pytest.raises(NotImplementedError):
            CompoundStep._run_steps(None, None, None)

        with pytest.raises(NotImplementedError):
            CompoundStep.run(None, None, None)
