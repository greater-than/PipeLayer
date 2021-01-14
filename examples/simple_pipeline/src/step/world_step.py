from steampipe.step import Step


class WorldStep(Step):

    def execute(self, context, data) -> str:
        return data + " World"
