import pytest


@pytest.mark.unit
class TestFilter:

    @pytest.mark.sad
    def test_filter_run_not_implemented(self):
        from pipelayer.filter import Filter
        with pytest.raises(NotImplementedError):
            Filter().run(None, None)
