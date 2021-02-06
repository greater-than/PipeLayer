import pytest


@pytest.mark.unit
class TestSealedClasses:

    @pytest.mark.sad
    def test_subclass_pipeline(self):
        from pipelayer import Pipeline
        with pytest.raises(TypeError):
            class MyPipeline(Pipeline):
                pass

    @pytest.mark.sad
    def test_subclass_switch(self):
        from pipelayer import Switch
        with pytest.raises(TypeError):
            class MySwitch(Switch):
                pass

    @pytest.mark.sad
    def test_filter_subclass(self):
        from pipelayer.filter import Filter
        with pytest.raises(TypeError):
            Filter()

    @pytest.mark.sad
    def test_filter_run_not_implemented(self):
        from pipelayer.filter import Filter
        with pytest.raises(NotImplementedError):
            Filter.run(None, None, None)
