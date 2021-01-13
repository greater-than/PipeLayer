from steampipe.step import Step


class HelloStep(Step):

    def execute(self, context) -> str:
        return "Hello"
