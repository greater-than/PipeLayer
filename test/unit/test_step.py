import pytest


@pytest.mark.unit
class TestStep:

    @pytest.mark.sad
    def test_step_run_not_implemented(self):
        from pipelayer.step import Step
        step = Step()

        with pytest.raises(NotImplementedError):
            step.run(None, None)
