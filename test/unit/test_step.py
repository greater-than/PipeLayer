import pytest


@pytest.mark.unit
class TestStep:

    @pytest.mark.sad
    def test_step(self):
        from pipelayer.step import Step
        with pytest.raises(NotImplementedError):
            Step.run(None, None, None)
