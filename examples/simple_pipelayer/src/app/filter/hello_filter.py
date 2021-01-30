from app.app_context import AppContext
from pipelayer import Filter


class HelloFilter(Filter):
    def run(self, context: AppContext, data: str = None) -> str:
        return "Hello"
