from pipelayer import Filter

from app.app_context import AppContext


class WorldFilter(Filter):
    def run(self, greeting: str, context: AppContext) -> str:
        return f"{greeting}, World."
