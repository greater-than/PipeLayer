import pytest


@pytest.mark.unit
class TestSubClass:

    @pytest.mark.sad
    def test_subclass_pipeline(self):
        from pipelayer import Pipeline
        with pytest.raises(TypeError):
            class MyPipeline(Pipeline):
                pass

    def test_subclass_switch(self):
        from pipelayer import Switch
        with pytest.raises(TypeError):
            class MySwitch(Switch):
                pass
