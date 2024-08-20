import pytest


@pytest.mark.unit
class TestDatetimeUtils:
    @pytest.mark.happy
    def test_get_now_utc(self):
        from pipelayer.utils.datetime_utils import get_now_utc

        d = get_now_utc()

        assert d
