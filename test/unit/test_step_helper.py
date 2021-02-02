import pytest
from pipelayer import StepHelper
from pipelayer.exception import InvalidFilterException


@pytest.mark.unit
class TestStepHelper:

    @pytest.mark.sad
    def test_initialize_step_none_step(self):
        with pytest.raises(InvalidFilterException):
            StepHelper.initialize_step(None)

    @pytest.mark.sad
    def test_initialize_step_invalid_step(self):
        with pytest.raises(InvalidFilterException):
            StepHelper.initialize_step(lambda a, b, c: a + b + c)

    @pytest.mark.sad
    def test_is_callable_valid_false(self):
        assert StepHelper._StepHelper__is_callable_valid(None) is False
        assert StepHelper._StepHelper__is_callable_valid("test") is False

    @pytest.mark.sad
    def test_is_run_static_false(self):
        class MyClass:
            def run(self, data, context):
                pass

        assert StepHelper._StepHelper__is_run_static(MyClass) is False

    @pytest.mark.sad
    def test_is_run_static_type_error(self):
        class MyClass:
            pass

        with pytest.raises(AttributeError):
            StepHelper._StepHelper__is_run_static(MyClass)
