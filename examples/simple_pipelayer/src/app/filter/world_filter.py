from app.app_context import AppContext
from pipelayer import Filter


class WorldFilter(Filter):

    def run(self, context: AppContext, data: str) -> str:
        return f"{data} World"
