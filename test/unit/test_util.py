import pytest


@pytest.mark.unit
class TestUtil:

    @pytest.mark.happy
    def test_render_manifest(self, manifest):
        from pipelayer.util import render_manifest

        assert render_manifest(manifest) == (
            '{\n  "name": "Pipeline",\n  "start": 1611261876.182439,\n  '
            '"end": 1611261880.49989,\n  "duration": "P0DT0H0M4.317451S",\n  "filters": [\n    '
            '{\n      "name": "FirstFilter",\n      "start": 1611261880.498892,\n      '
            '"end": 1611261880.498892,\n      "duration": "P0DT0H0M0.000000S",\n      '
            '"pre_process": null,\n      "post_process": null\n    },\n    {\n      '
            '"name": "second_filter",\n      "start": 1611261880.498892,\n      '
            '"end": 1611261880.498892,\n      "duration": "P0DT0H0M0.000000S",\n      '
            '"pre_process": null,\n      "post_process": null\n    },\n    {\n      '
            '"name": "lambda context, data: json.dumps(data)",\n      '
            '"start": 1611261880.498892,\n      "end": 1611261880.49989,\n      '
            '"duration": "P0DT0H0M0.000998S",\n      "pre_process": null,\n      '
            '"post_process": null\n    }\n  ]\n}')
