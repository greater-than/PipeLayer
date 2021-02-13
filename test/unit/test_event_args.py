import pytest


@pytest.mark.unit
class TestEventArgs:

    @pytest.mark.happy
    def test_event_args_getters(self):
        from pipelayer import Context, State
        from pipelayer.enum import Action
        from pipelayer.event_args import FilterEventArgs

        evt_args = FilterEventArgs("test", Context(), State.RUNNING)

        assert evt_args.data == "test"
        assert isinstance(evt_args.context, Context)
        assert evt_args.state is State.RUNNING
        assert evt_args.action is Action.CONTINUE

    @pytest.mark.happy
    def test_event_args_setters(self):
        from pipelayer import Context, State
        from pipelayer.enum import Action
        from pipelayer.event_args import FilterEventArgs

        evt_args = FilterEventArgs("test", Context(), State.RUNNING)

        evt_args.data = "TEST"
        evt_args.action = Action.EXIT

        assert evt_args.data == "TEST"
        assert isinstance(evt_args.context, Context)
        assert evt_args.state is State.RUNNING
        assert evt_args.action is Action.EXIT
