from typing import Any

from steampipe import Manifest
from steampipe.util import render_manifest


def print_manifest(manifest: Manifest) -> None:
    print("")
    print("==================")
    print("Pipeline Manifest:")
    print("------------------")
    print(render_manifest(manifest))
    print("")


def print_output(output: Any) -> None:
    print("")
    print("==================")
    print("Pipeline Output:")
    print("------------------")
    print(output)
    print("")
