import json
from typing import Any


def print_manifest(manifest: str) -> None:
    print("")
    print("==================")
    print("Pipeline Manifest:")
    print("------------------")
    print(json.dumps(json.loads(manifest), indent=2))
    print("")


def print_output(output: Any) -> None:
    print("")
    print("==================")
    print("Pipeline Output:")
    print("------------------")
    print(output)
    print("")
