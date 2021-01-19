import pytest


@pytest.mark.unit
class TestApp:
    def test_app(self, mocker):
        from app.app import main
        main()
        assert True
