from typing import Any

from pipelayer import Manifest
from pipelayer.util import render_manifest


class Color:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_manifest(manifest: Manifest) -> None:
    _render("MANIFEST", render_manifest(manifest))


def print_output(output: Any) -> None:
    _render("OUTPUT", output)


def _render(message: str, output: Any) -> None:
    print(f"{Color.OKCYAN}--------------------------------------------------------------------------------{Color.ENDC}")
    print(f"{Color.OKGREEN}{message}:{Color.ENDC}\n")
    print(output + "\n")
