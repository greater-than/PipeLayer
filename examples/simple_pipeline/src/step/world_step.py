from app_context import AppContext
from steampipe import Step


class WorldStep(Step):

    def run(self, context: AppContext, data: str) -> str:
        return f"{data} World"
