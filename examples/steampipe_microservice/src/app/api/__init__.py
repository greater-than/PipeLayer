from typing import cast

from app.exception import HttpException


def handle_exception(e: Exception) -> dict:

    if isinstance(e, [HttpException]):
        e: HttpException = cast(HttpException, e)
        return {
            "statusCode": e.http_status_code,
            "message": str(e)
        }
    else:
        return {
            "statusCode": 500,
            "message": "An unhandled exception occured"
        }
