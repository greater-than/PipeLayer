from pipelayer import Filter

from app.app_context import AppContext


class WorldFilter(Filter):

    def run(self, context: AppContext, data: str) -> str:
        return f"{data} World"
