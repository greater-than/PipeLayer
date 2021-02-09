from app.app_context import AppContext
from pipelayer import Filter


class WorldFilter(Filter):
    def run(self, greeting: str, context: AppContext) -> str:
        return f"{greeting}, World."
