import pytest


@pytest.mark.unit
class TestFilter:

    def test_filter_interface_implemented(self):
        from pipelayer.filter import Filter
        from pipelayer.protocol import Step

        class MyFilter(Filter):
            def run(data, context):
                pass

        assert isinstance(MyFilter(), Step)
