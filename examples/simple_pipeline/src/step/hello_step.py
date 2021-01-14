from steampipe.step import Step


class HelloStep(Step):

    def execute(self, context, data) -> str:
        return "Hello"
