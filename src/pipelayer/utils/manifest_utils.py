import json

from pipelayer.manifest import Manifest


def render_manifest(manifest: Manifest, indent: int = 2) -> str:
    """
    Renders a formatted Manifest
    """
    manifest_str = manifest.model_dump_json()
    manifest_dict = json.loads(manifest_str)
    return json.dumps(manifest_dict, indent=indent)
