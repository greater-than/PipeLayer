import datetime

import pytest


@pytest.mark.unit
class TestEventArgs:

    @pytest.mark.happy
    def test_pipeline_event_args_getters(self):
        from pipelayer.enum import StepType
        from pipelayer.event_args import PipelineEventArgs
        from pipelayer.manifest import Manifest

        evt_args: PipelineEventArgs = PipelineEventArgs(
            "step_name",
            "test",
            Manifest(name="test", step_type=StepType.FILTER, start=datetime.datetime.now())
        )

        assert evt_args.step_name == "step_name"
        assert evt_args.data == "test"
        assert isinstance(evt_args.manifest_entry, Manifest)

    @pytest.mark.happy
    def test_pipeline_event_args_setters(self):
        from pipelayer.enum import StepType
        from pipelayer.event_args import PipelineEventArgs
        from pipelayer.manifest import Manifest

        evt_args: PipelineEventArgs = PipelineEventArgs(
            "step_name",
            "test",
            Manifest(name="test", step_type=StepType.FILTER, start=datetime.datetime.now())
        )

        evt_args.data = "test"

        assert evt_args.step_name == "step_name"
        assert evt_args.data == "test"
        assert isinstance(evt_args.manifest_entry, Manifest)

    @pytest.mark.happy
    def test_filter_event_args_getters(self):
        from pipelayer import Context, State
        from pipelayer.enum import Action
        from pipelayer.event_args import FilterEventArgs

        evt_args = FilterEventArgs("test", Context(), State.RUNNING)

        assert evt_args.data == "test"
        assert isinstance(evt_args.context, Context)
        assert evt_args.state is State.RUNNING
        assert evt_args.action is Action.CONTINUE

    @pytest.mark.happy
    def test_filter_event_args_setters(self):
        from pipelayer import Context, State
        from pipelayer.enum import Action
        from pipelayer.event_args import FilterEventArgs

        evt_args = FilterEventArgs("test", Context(), State.RUNNING)

        evt_args.data = "test"
        evt_args.action = Action.EXIT

        assert evt_args.data == "test"
        assert isinstance(evt_args.context, Context)
        assert evt_args.state is State.RUNNING
        assert evt_args.action is Action.EXIT
