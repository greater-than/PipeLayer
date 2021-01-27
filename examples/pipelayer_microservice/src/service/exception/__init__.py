class ResponseException(Exception):
    def __init__(self, http_status_code: int, *args) -> None:
        super().__init__(*args)
        self.__http_status_code = http_status_code

    @property
    def http_status_code(self) -> int:
        return self.__http_status_code


class ApplicationException(ResponseException):
    def __init__(*args):
        super().__init__(http_status_code=500, *args)
