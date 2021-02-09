import json

from pipelayer.manifest import StepManifest


def render_manifest(manifest: StepManifest, indent: int = 2) -> str:
    """
    Renders a formatted Manifest
    """
    manifest_str = manifest.json()
    manifest_dict = json.loads(manifest_str)
    return json.dumps(manifest_dict, indent=indent)
