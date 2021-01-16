import json

from pipelayer.manifest import Manifest


def render_manifest(manifest: Manifest, indent: int = 2) -> str:
    manifest_str = manifest.json()
    manifest_dict = json.loads(manifest_str)
    return json.dumps(manifest_dict, indent=indent)
