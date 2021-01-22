import pytest
from pipelayer import Context


@pytest.mark.unit
class TestContext:

    @pytest.mark.sad
    def test_invalid_context_implementation(self):
        class InvalidContext(Context):
            pass

        with pytest.raises(TypeError):
            InvalidContext()
