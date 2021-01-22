class InvalidFilterException(Exception):
    pass


class PipelineException(Exception):
    def __init__(self, inner_exception: Exception, *args: object) -> None:
        super().__init__(inner_exception, *args)
        self.__inner_exception = inner_exception

    @property
    def inner_exception(self) -> Exception:
        return self.__inner_exception
