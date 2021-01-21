from pipelayer import Filter

from app.app_context import AppContext


class HelloFilter(Filter):
    def run(self, context: AppContext, data: str = None) -> str:
        return "Hello"
