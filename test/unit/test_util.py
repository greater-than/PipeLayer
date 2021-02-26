import pytest


@pytest.mark.unit
class TestUtil:

    @pytest.mark.happy
    def test_render_manifest(self, manifest):
        from pipelayer.util import render_manifest

        should_be = (
            '{\n  "name": "Pipeline",\n'
            '  "step_type": "Pipeline",\n'
            '  "start": 1611261876.182439,\n'
            '  "end": 1611261880.49989,\n'
            '  "duration": "P0DT0H0M4.317451S",\n'
            '  "steps": [\n    {\n'
            '      "name": "FirstFilter",\n'
            '      "step_type": "Filter",\n'
            '      "start": 1611261880.498892,\n'
            '      "end": 1611261880.498892,\n'
            '      "duration": "P0DT0H0M0.000000S"\n    },\n    {\n'
            '      "name": "second_filter",\n'
            '      "step_type": "Filter",\n'
            '      "start": 1611261880.498892,\n'
            '      "end": 1611261880.498892,\n'
            '      "duration": "P0DT0H0M0.000000S"\n    },\n    {\n'
            '      "name": "[lambda data, context: json.dumps(data)]",\n'
            '      "step_type": "Filter",\n'
            '      "start": 1611261880.498892,\n'
            '      "end": 1611261880.49989,\n'
            '      "duration": "P0DT0H0M0.000998S"\n    }\n  ]\n}'
        )
        assert render_manifest(manifest) == should_be
