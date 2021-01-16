import json
from typing import Any

from pipelayer.context import Context
from pipelayer.filter import Filter
from pipelayer.manifest import Manifest


class MockFilter(Filter):
    """
    For patching pipeline filters in unit tests
    """

    def run(self, context: Context, data: Any) -> Any:
        return data


def render_manifest(manifest: Manifest, indent: int = 2) -> str:
    """
    Renders a formatted Manifest
    """
    manifest_str = manifest.json()
    manifest_dict = json.loads(manifest_str)
    return json.dumps(manifest_dict, indent=indent)
