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
    def test_is_callable_valid(self):
        def func(data, Context):
            return True
        assert StepHelper.is_callable_valid(func)

    @pytest.mark.sad
    def test_is_callable_valid_false(self):
        assert StepHelper.is_callable_valid(None) is False
        assert StepHelper.is_callable_valid("test") is False

    @pytest.mark.sad
    def test_is_class_func_static_false(self):
        class MyClass:
            def run(self, data, context):
                pass

        assert StepHelper._StepHelper__is_class_func_static(MyClass) is False

    @pytest.mark.sad
    def test_is_class_func_static_type_error(self):
        class MyClass:
            pass

        with pytest.raises(AttributeError):
            StepHelper._StepHelper__is_class_func_static(MyClass)

    @pytest.mark.happy
    def test_is_class_func_static(self):
        from pipelayer.filter import Filter

        class MyClass(Filter):
            @staticmethod
            def run(data, context):
                pass

        assert StepHelper._StepHelper__is_class_func_static(MyClass)

    @pytest.mark.happy
    def test_is_class_func_static_using_instance(self):
        from pipelayer.filter import Filter

        class MyClass(Filter):
            @staticmethod
            def run(data, context):
                pass

        assert StepHelper._StepHelper__is_class_func_static(type(MyClass()))
