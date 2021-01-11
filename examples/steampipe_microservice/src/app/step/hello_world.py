from app.config.app_context import AppContext
from steampipe.step import Step


class HelloWorld(Step):
    def execute(context: AppContext) -> str:
        return "Hello World"

    class PostProcess:

        @staticmethod
        def create_response(context: AppContext, data: str) -> dict:
            return {
                "message": data
            }
