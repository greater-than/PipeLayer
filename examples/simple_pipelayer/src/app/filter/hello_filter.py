from typing import Any

from app.app_context import AppContext
from pipelayer import Filter


class HelloFilter(Filter):
    def run(self, data: Any, context: AppContext) -> str:
        return "Hello"
