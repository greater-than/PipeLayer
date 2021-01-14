from app_context import AppContext
from steampipe import Step


class HelloStep(Step):

    def run(self, context: AppContext, data: str = None) -> str:
        return "Hello"
