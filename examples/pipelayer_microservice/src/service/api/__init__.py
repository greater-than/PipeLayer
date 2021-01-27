from logging import Logger
from typing import cast

from service.exception import ResponseException


def handle_exception(e: Exception, log: Logger = Logger("Error Logger")) -> dict:
    log.error("Error")
    if isinstance(e, [ResponseException]):
        e: ResponseException = cast(ResponseException, e)
        log.error("{str(e)}", exc_info=e, http_status_code=e.http_status_code)
        return {
            "statusCode": e.http_status_code,
            "message": str(e)
        }
    else:
        log.error("Unhandled Exception", exc_info=e)
        return {
            "statusCode": 500,
            "message": "An unhandled exception occured"
        }
